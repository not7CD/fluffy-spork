""" Collection of scripts to help organize large batches of document images. """
import os
import subprocess
from datetime import datetime
from pymongo import MongoClient

import populatedb
import numbermanualy
import rotate
import cleanimage
import resize


def preprocess(my_db, args):
    """Preporcessing of images before OCR"""
    substep_queue = []

    substep = rotate.rotate_img
    substep_queue.append(
        (
            substep,
            'rotate',
            os.path.join(args.paths['preprocess'], str(substep.__name__)),
            {"steps." + str(substep.__name__): {"$exists": False}}
        ))

    substep = resize.resize_300dpi
    substep_queue.append(
        (
            substep,
            'rotate_img',
            os.path.join(args.paths['preprocess'], str(substep.__name__)),
            {"steps." + str(substep.__name__): {"$exists": False}}
        ))
    substep = cleanimage.imagemagic_textcleaner
    substep_queue.append(
        (
            substep,
            'resize_300dpi',
            os.path.join(args.paths['preprocess'], str(substep.__name__)),
            {"steps." + str(substep.__name__): {"$exists": False}}
        ))

    for step, previous_step, step_outpath, step_query in substep_queue:
        print('Running step: %s' % (step.__name__))
        if not os.path.exists(step_outpath):
            os.makedirs(step_outpath)
        feh = subprocess.Popen(['feh', 'tmp.jpg'])
        document = my_db.documents.find_one(step_query)
        while document is not None:
            if True:
                this = {"file_name": document['file_name']}
                substep_input_path = document['steps'][previous_step]['path']
                substep_output_path = os.path.join(
                    step_outpath, document['file_name'])
                tags = None
                if 'tags' in document:
                    tags = document['tags']
                step_data = None
                if 'data' in document['steps'][previous_step]:
                    step_data = document['steps'][previous_step]['data']
                # print(document['steps'][previous_step])
                # print(step_data)
                step_data = step(substep_input_path, substep_output_path,
                                 step_data, tags=tags)
                feh.kill()
                feh = subprocess.Popen(['feh', substep_output_path])
                update = {
                    "$set": {
                        "steps." + str(step.__name__): {
                            "data": step_data,
                            "path": substep_output_path,
                            "date": datetime.now()
                        }
                    }
                }
                # print(update)
                # , '$unset': {'tags.flip': None}
                result = my_db.documents.update_one(this, update)
                if result.modified_count > 0:
                    print('%s: %s with %s' %
                          (str(step.__name__), this['file_name'], step_data))
        feh.kill()
        document = my_db.documents.find_one(step_query)



def clean_add_tags(document):
    document['steps']['numbermanualy']['data']


def process(my_db, args):
    """Data extraction from images"""
    clean_query = {"$or": [{"steps.numbermanualy.data": 'flip'}, {
        "steps.numbermanualy.data": 'horizontal'}]}
    cursor = my_db.documents.find(clean_query)
    for document in cursor:
        this = {"file_name": document['file_name']}
        tags = {}
        try:
            if 'tags' in document:
                tags = document['tags']
        except TypeError:
            pass
        try:
            if 'flip' in document['steps']['numbermanualy']['data']:
                tag = 'flip'
                tags[tag] = 0
        except TypeError:
            pass
        update = {"$set": {"steps.numbermanualy.data": ""},
                  "$unset": {"flip": 0}}
        update["$set"].update({'tags': tags})
        print(update)
        result = my_db.documents.update_one(this, update)

    substep_queue = [
        (numbermanualy.process_manualy,
         {"$or": [{"steps.numbermanualy": {"$exists": False}}, {"steps.numbermanualy.data": ""}]})
    ]
    for substep, query in substep_queue:
        cursor = my_db.documents.find(query)
        i_left = cursor.count()
        for document in cursor:
            this = {"file_name": document['file_name']}
            data = substep(document)
            i_left -= 1

            print('Got: %s, (%s left)' % (data, i_left))

            update = {
                "$set": {
                    "steps.numbermanualy": {
                        "data": data,
                        "date": datetime.now()
                    }
                }
            }
            result = my_db.documents.update_one(this, update)
            if result.modified_count > 0:
                print('succ')


def sort(my_db, args):
    """Sort images based on extrated data"""
    pass


def main(args):
    client = MongoClient()
    db = client[args.database['name']]

    step_queue = (preprocess, process, sort)

    if args.add_paths is not None:
        for path in args.add_paths:
            populatedb.add_dir_db(db, path)
    for step in step_queue:
        step(db, args)


if __name__ == '__main__':
    import config as config_file
    main(config_file)
