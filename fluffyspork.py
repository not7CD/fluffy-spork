""" Collection of scripts to help organize large batches of document images. """
import os
import subprocess
from datetime import datetime
from pymongo import MongoClient
import time

import populatedb
import numbermanualy
import rotate
import cleanimage
import resize
import extract


def clean_tags(inpath=None, outpath=None, data=None, tags=None):
    set_dict = {}
    set_dict["date"] = datetime.now()
    unset_dict = {
        'steps.simple_regexr.tags': None
    }
    return (set_dict, unset_dict)


def exec_step(step_tulpe, document):
    step, previous_step, step_outpath, step_query = step_tulpe
    substep_output_path = os.path.join(
        step_outpath, document['file_name'])
    try:
        substep_input_path = document['steps'][previous_step]['path']
    except KeyError as e:
        substep_input_path = substep_output_path
        print(e)
    tags = None
    if 'tags' in document:
        tags = document['tags']
    step_data = None
    if 'data' in document['steps'][previous_step]:
        step_data = document['steps'][previous_step]['data']
    step_data = step(substep_input_path, substep_output_path,
                     step_data, tags=tags)

    set_dict = unset_dict = None
    if isinstance(step_data, dict):
        set_dict = step_data
    elif isinstance(step_data, tuple):
        set_dict, unset_dict = step_data
    else:
        set_dict = {
            "data": step_data,
            "path": substep_output_path
        }
        set_dict["date"] = datetime.now()
    if set_dict == {}:
        update = None
    else:
        update = {"$set": {"steps." + str(step.__name__): set_dict}}
        if unset_dict is not None:
            update["$unset"] = unset_dict
    return update


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
    substep = extract.simple_tesseract
    substep_queue.append(
        (
            substep,
            'imagemagic_textcleaner',
            os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
            {"steps." + str(substep.__name__): {"$exists": False}}
        ))

    substep = extract.simple_regexr
    substep_queue.append(
        (
            substep,
            'simple_tesseract',
            os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
            {"$or": [
                {"steps." + str(substep.__name__): {"$exists": False}},
                {"steps." + str(substep.__name__) +
                 ".tags": {"$exists": False}}
            ]}
        ))
    substep = clean_tags
    substep_queue.append(
        (
            substep,
            'simple_regexr',
            os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
            {"steps.simple_regexr.tags": {"$exists": True}}
        ))

    for substep_in_queue in substep_queue:
        print('== Running step: %s' % (substep_in_queue[0].__name__))
        if not os.path.exists(substep_in_queue[2]):
            os.makedirs(substep_in_queue[2])
        document = my_db.documents.find_one(substep_in_queue[-1])
        data_str = 'No update'
        while document is not None:
            update = exec_step(substep_in_queue, document)
            # print(update)
            if update is not None:
                result = my_db.documents.update_one(document, update, upsert=True)
                if result.modified_count > 0:
                    data_str = update
            print('=== %s: %s with %s' %
                  (str(substep_in_queue[0].__name__), document['file_name'], data_str))
            # time.sleep(0.05)

            document = my_db.documents.find_one(substep_in_queue[-1])


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
