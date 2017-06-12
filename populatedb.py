"""Initial step. Add files from directory to data base."""
import os
from datetime import datetime
# from pymongo import MongoClient
from processdirectory import process_directory

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
