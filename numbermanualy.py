"""File: number-manualy.py
    Author: Norbert Szulc `not7CD`
    Open image and let user input its number manualy,
    then save it under new name in output directory.
"""


import re
import subprocess
import time
import datetime

from PIL import Image

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np

PICTURE_RE = re.compile(r'.*\.jpg$', re.IGNORECASE)


def input_from_user(path):
    """Opens path with feh, waits for input from user"""
    feh = subprocess.Popen(['feh', path])
    # show massage in command line and ask for number shown in feh
    time.sleep(0.1)
    subprocess.call(['xdotool', 'click', '1'])
    print("Input number from image:")
    number = input()
    feh.kill()
    return str(number)


def process_manualy(document):
    """Returns str"""
    path = document['steps']['rotate']['path']
    with Image.open(path) as img:
        size = 730, 730
        width = img.size[0]
        # img_tmp = img.thumbnail(size)
        # img_tmp.save('tmp.jpg')
        img = img.crop((0, 0, width, width))
        img.thumbnail(size)
        img.save('tmp.jpg')
        return input_from_user('tmp.jpg')

def number_manualy(my_db, args):
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
        (process_manualy,
         {"$or": [{"steps.numbermanualy": {"$exists": False}}, {"steps.numbermanualy.data": ""}]})
    ]
    for substep, query in substep_queue:
        cursor = my_db.documents.find(query)
        query_size = cursor.count()
        for index, document in enumerate(cursor):
            this = {"file_name": document['file_name']}
            data = substep(document)


            print('(%s/%s) Got: %s'  % (data, index, query_size))

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

    clean_query = {"steps.simple_regexr.data": {'$exists' : True}}
    cursor = my_db.documents.find(clean_query)
    for document in cursor:
        try:
            print('=====================================\n',document['steps']['simple_regexr']['data']['UNIT3_RE'])
        except KeyError as e:
            pass
        # for key, value in document['steps']['simple_regexr']['data'].items():
        #     print(key, value)
