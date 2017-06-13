"""File: number-manualy.py
    Author: Norbert Szulc `not7CD`
    Open image and let user input its number manualy,
    then save it under new name in output directory.
"""


import re
import subprocess
import time

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
