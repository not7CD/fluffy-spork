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
import create_dict
import bruteforce


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
    if set_dict == {}:
        update = None
    else:
        set_dict["date"] = datetime.now()
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
    # substep = cleanimage.imagemagic_textcleaner
    # substep_queue.append(
    #     (
    #         substep,
    #         'resize_300dpi',
    #         os.path.join(args.paths['preprocess'], str(substep.__name__)),
    #         {"steps." + str(substep.__name__): {"$exists": False}}
    #     ))
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
    # substep = clean_tags
    # substep_queue.append(
    #     (
    #         substep,
    #         'simple_regexr',
    #         os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
    #         {"steps.simple_regexr.tags": {"$exists": True}}
    #     ))
    timeOld = datetime.today().replace(hour=14, minute=45)
    substep = bruteforce.levenshtein
    substep_queue.append(
        (
            substep,
            'simple_tesseract',
            os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
            {"$or": [
                {"steps." + str(substep.__name__): {"$exists": False}},
                {"steps." + str(substep.__name__): None}
                 ]}
        ))
    substep = bruteforce.job_titles
    substep_queue.append(
        (
            substep,
            'simple_tesseract',
            os.path.join(args.paths['preprocess'], 'imagemagic_textcleaner'),
            {"$or": [
                {"steps." + str(substep.__name__): {"$exists": False}},
                {"steps." + str(substep.__name__): None},
                {"steps." + str(substep.__name__)+ ".date": {"$lt": timeOld}}
                 ]}
        ))

    for substep_in_queue in substep_queue:
        print('== Running step: %s' % (substep_in_queue[0].__name__))
        if not os.path.exists(substep_in_queue[2]):
            os.makedirs(substep_in_queue[2])
        document = my_db.documents.find_one(substep_in_queue[-1])
        data_str = 'No update'
        index_left = my_db.documents.find(substep_in_queue[-1]).count()
        while document is not None:
            index_left -= 1
            update = exec_step(substep_in_queue, document)
            if update is not None:
                result = my_db.documents.update_one(
                    document, update, upsert=True)
                if result.modified_count > 0:
                    data_str = update
            print('=== %s left ===\n=== %s: %s\n%s' %
                  (index_left, str(substep_in_queue[0].__name__), document['file_name'], data_str))

            document = my_db.documents.find_one(substep_in_queue[-1])


def sort(my_db, args):
    """Sort images based on extrated data"""
    substep_queue = []


def main(args):
    client = MongoClient()
    db = client[args.database['name']]

    step_queue = (preprocess, sort)

    if args.add_paths is not None:
        for path in args.add_paths:
            populatedb.add_dir_db(db, path)
    for step in step_queue:
        step(db, args)


if __name__ == '__main__':
    import config as config_file
    main(config_file)
