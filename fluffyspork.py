""" Collection of scripts to help organize large batches of document images. """
import os
# import re
from datetime import datetime
from pymongo import MongoClient

import populatedb
import numbermanualy
import rotate


def preprocess(my_db, args):
    """Preporcessing of images before OCR"""

    query = {
        "$and": [{"steps.rotate.data": {"$exists": False}},
                 {"$or": [{"steps.rotate": {"$exists": False}}, {"tags.flip": {"$exists": True}}]
                  }]
    }

    substep_path = os.path.join(
        args.paths['preprocess'], str(rotate.__name__))
    # print(substep_path)
    if not os.path.exists(substep_path):
        os.makedirs(substep_path)

    cursor = my_db.documents.find(query)
    for document in cursor:
        this = {"file_name": document['file_name']}
        substep_input_path = document['steps']['raw']['path']
        substep_output_path = os.path.join(substep_path, document['file_name'])
        tags = None
        if 'tags' in document:
            tags = document['tags']

        rotation = 0
        rotation = rotate.process_img(
            substep_input_path, substep_output_path, rotation=rotation, tags=tags)
        update = {
            "$set": {
                "steps.rotate": {
                    "data": rotation,
                    "path": substep_output_path,
                    "date": datetime.now()
                }
            }
        }
        # , '$unset': {'tags.flip': None}
        result = my_db.documents.update_one(this, update)
        if result.modified_count > 0:
            print('%s: %s' % (str(rotate.__name__),this))


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
