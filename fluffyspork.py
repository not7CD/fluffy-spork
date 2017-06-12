""" Collection of scripts to help organize large batches of document images. """
import os
import re
from datetime import datetime
from pymongo import MongoClient


PICTURE_RE = re.compile(r'.*\.jpg$', re.IGNORECASE)

def process_directory(db, path, fun, recursive=False):
    """ Process all elements in directory, """

    if not os.path.isdir(path):
        print(path, 'is not a directory!')
    else:
        for element in os.listdir(path):
            element_path = os.path.join(path, element)
            if os.path.isdir(element_path) and recursive:
                process_directory(db, element_path, fun, recursive)

            elif os.path.isfile(element_path) and re.match(PICTURE_RE, element_path):
                fun(db, element_path)


def lambda_add_path(db, path):
    tail = os.path.basename(path)
    cursor = db.documents.find_one({"file_name": tail})
    # print(cursor)
    if cursor is not None:
        print('skip: %s' % (tail))
    else:

        result = db.documents.insert_one(
            {
                "file_name": tail,
                "employee": {"id": None,
                             "unit": None,
                             "job_title": None},
                "steps": {
                    "raw": {
                        "path": path,
                        "date": datetime.now()
                    }
                }
            }
        )
        print('created %s with %s' % (tail, result.inserted_id))


def add_dir_db(db, path):
    process_directory(db, path, lambda_add_path, True)


def main(args):
    client = MongoClient()
    db = client[args.database['name']]

    if args.add_paths is not None:
        for path in args.add_paths:
            add_dir_db(db, path)


if __name__ == '__main__':
    import config as config_file
    main(config_file)
