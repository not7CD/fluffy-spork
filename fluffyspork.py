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
    cursor = my_db.documents.find({"steps.rotate": {"$exists": False}})

    substep_path = os.path.join(args.paths['preprocessed'], str(rotate.__name__))
    print(substep_path)
    if not os.path.exists(substep_path):
        os.makedirs(substep_path)

    for document in cursor:
        # print(document)
        substep_output_path = os.path.join(substep_path, document['file_name'])
        print(substep_output_path)
        rotate.process_img(
            document['steps']['raw']['path'], substep_output_path)
        result = my_db.documents.update_one(
            {"file_name": document['file_name']},
            {
                "$set": {
                    "steps.rotate": {
                        "path": substep_output_path,
                        "date": datetime.now()
                    },

                }
            }
        )
        # print('Got: %s' % elt_id)


def process(my_db, args):
    """Data extraction from images"""
    cursor = my_db.documents.find({"steps.numbermanualy": {"$exists": False}})
    i_left = cursor.count()
    for document in cursor:
        # print(document)
        elt_id = numbermanualy.process_manualy(
            document['steps']['rotate']['path'])
        i_left -= 1
        print('Got: %s, (%s left)' % (elt_id, i_left))
        result = my_db.documents.update_one(
            {"file_name": document['file_name']},
            {
                "$set": {
                    "steps.numbermanualy": {
                        "data": elt_id,
                        "date": datetime.now()
                    },

                }
            }
        )


def sort(my_db, args):
    """Sort images based on extrated data"""
    pass


def main(args):
    client = MongoClient()
    db = client[args.database['name']]

    STEP_QUEUE = (preprocess, process, sort)

    if args.add_paths is not None:
        for path in args.add_paths:
            populatedb.add_dir_db(db, path)
    for step in STEP_QUEUE:
        step(db, args)


if __name__ == '__main__':
    import config as config_file
    main(config_file)
