import os
from PIL import Image
from pymongo import MongoClient

MAIN_DIR = 'data/sorted_test'


def main(my_db, query):
    cursor = my_db.documents.find(query)
    for document in cursor:
        im_path = document['steps']['resize_300dpi']['path']
        data_num, data_dep = (document['steps']['numbermanualy']['data'],
                              document['steps']['manualcheck']['data']['departament'])

        if data_dep != "???":
            data_dep = data_dep['match']['departament-code'] + \
                " " + data_dep['match']['departament-name']
        new_path = os.path.join(MAIN_DIR, data_dep)
        if not os.path.exists(new_path):
            os.makedirs(new_path)
        new_path = os.path.join(new_path, data_num + "_" + document['file_name'])
        with Image.open(im_path) as im:
            print("->", new_path)
            im.save(new_path)


if __name__ == '__main__':
    DATABASE_NAME = 'fluffyspork'
    QUERY = {"steps.manualcheck.data": {"$exists": True}}
    client = MongoClient()
    db = client[DATABASE_NAME]
    main(db, QUERY)
