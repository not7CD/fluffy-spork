"""Show picture, ask operator to check data."""

from PIL import Image
# import bruteforce
import subprocess

def show_image(path):
    # opens image viewer
    iv_instance = subprocess.Popen(['feh', path])
    # simple workaround to refocus console
    time.sleep(0.1)
    subprocess.call(['xdotool', 'click', '1'])
    # returns imageviewer so it can be later called to for kill()
    return iv_instance

def resize_image(path):
    return tmp_path

def main(db_name):

    cursor = my_db.documents.find(query)
    for document in cursor:
        im_path
        iv = show_image(resize_image())

    pass

if __name__ == '__main__':
    DATABASE_NAME = {'name': 'fluffyspork'}
    main(DATABASE_NAME)
