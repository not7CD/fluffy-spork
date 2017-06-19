"""Show picture, ask operator to check data."""

import subprocess
import time
from PIL import Image
from pymongo import MongoClient
from blendercolors import bcolors
import bruteforce


def show_image(path):
    # opens image viewer
    iv_instance = subprocess.Popen(['feh', path])
    # simple workaround to refocus console
    time.sleep(0.1)
    subprocess.call(['xdotool', 'click', '1'])
    # returns imageviewer so it can be later called to for kill()
    return iv_instance


def resize_image(path):
    with Image.open(path) as img:
        size = 730, 730
        width = img.size[0]
        # img = img.crop((0, 0, width, width))
        img.thumbnail(size)
        img.save('tmp.jpg')
    return 'tmp.jpg'


def highlight_str(string, i_start, i_stop=None, length=None):
    if length is not None:
        i_stop = i_start + length + 1
    if i_stop is None:
        i_stop = len(string)
    highlighted = string[:i_start] + bcolors.WARNING + \
        string[i_start:i_stop] + bcolors.ENDC + string[i_stop:]
    return highlighted


def highlight_data(source_data, match_data):
    match_index = source_data.index(match_data['sentence'])
    full_string = highlight_str(source_data, match_index,
                                length=len(match_data['sentence']))
    match_string = highlight_str(match_data['match'], 0)
    # match_string = highlight_str(match_data['match']['departament-name'], 0)
    return (full_string, match_string)


def human_validate(compare, raw):
    full_data_r, match_data_r = raw
    print(('\n=============\n%s\n------------\n%s\n------------\n' +
           'Is this data correct? ([y]/n)') % compare)
    not_robot_input = input()
    print(repr(not_robot_input))
    if not_robot_input == '' or not_robot_input == 'y':
        return match_data_r
    else:
        print("Give proper name:")
        not_robot_name = input()
        if not_robot_name == "???":
            return not_robot_name
        else:
            not_robot_name += '                  '
            bfc = bruteforce.job_titles(data=not_robot_name)
            # print(bfc)
            # dirty fix
            cmp = highlight_data(not_robot_name, bfc[0]['data'])
            return human_validate(cmp, (not_robot_name, bfc[0]['data']))


def main(my_db, query):
    cursor = my_db.documents.find(query)
    for document in cursor:
        im_path = document['steps']['resize_300dpi']['path']
        iv_instance = show_image(resize_image(im_path))
        data = (document['steps']['simple_tesseract']['data'],
                document['steps']['job_titles']['data'])
        highlighted = highlight_data(data[0], data[1])
        validated = human_validate(highlighted, data)

        print("->", validated)
        update = {"$set": {"steps.manualcheck.data.job_title": validated}}
        if update is not None:
            my_db.documents.update_one(
                document, update, upsert=True)

        # kill imageviewer or you will be flooded!
        iv_instance.kill()


if __name__ == '__main__':
    DATABASE_NAME = 'fluffyspork'
    QUERY = {"steps.manualcheck.data.job_title": {"$exists": False}}
    client = MongoClient()
    db = client[DATABASE_NAME]
    main(db, QUERY)
