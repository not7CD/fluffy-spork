""" Collection of scripts to help organize large batches of document images. """
# import os
# import re
# from datetime import datetime
from pymongo import MongoClient

import populatedb
import numbermanualy

def preprocess(db):
    pass

def process(db):
    pass

def sort(db):
    pass

def main(args):
    client = MongoClient()
    db = client[args.database['name']]

    STEP_QUEUE = (preprocess, process, sort)

    if args.add_paths is not None:
        for path in args.add_paths:
            populatedb.add_dir_db(db, path)
    for step in STEP_QUEUE:
        step(db)


if __name__ == '__main__':
    import config as config_file
    main(config_file)
