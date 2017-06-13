"""
    File: rotate.py
    Author: Norbert Szulc `not7CD`
    Batch image rotation depending on thier width-height ratio
"""

import argparse
import os
import re
# import cv2

from PIL import Image

PICTURE_RE = re.compile(r'.*\.jpg$', re.IGNORECASE)


def determine_rotation(size, tags=None):
    """Returns original rotation from expected"""
    rotation = 0
    width, height = size
    if width > height:
        rotation += 90
    try:
        if 'flip' in tags:
            rotation += 180
    except TypeError:
        pass
    return rotation



def process_img(path, output_path, rotation=0, tags=None):
    """ This function rotates images to portrait rotation """
    with Image.open(path) as img:
        if rotation == 0:
            rotation = determine_rotation(img.size, tags)
        img = img.rotate(-rotation, expand=True)
        img.save(output_path)
    return rotation


def process_dir(path, output_path=None, recursive=False):
    """ Process all elements in directory, output processed in given output dir."""
    if not output_path:
        output_path = path

    if not os.path.isdir(path):
        print(path, 'is not a directory!')
    else:
        for element in os.listdir(path):
            element_path = os.path.join(path, element)
            element_output_path = os.path.join(output_path, element)

            if os.path.isdir(element_path) and recursive:
                process_dir(element_path, output_path, recursive)

            elif os.path.isfile(element_path) and re.match(PICTURE_RE, element_path):
                print("Rotating %s, saving to %s" % (element, output_path))
                process_img(element_path, element_output_path)


def main(args):
    """ Process all given directories """
    for directory in args['dir']:
        process_dir(directory, args['output'], args['recursive'])

if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--dir', '-d', nargs='+')
    PARSER.add_argument('--output', '-o')
    PARSER.add_argument('--recursive', '-r', action='store_true')

    ARGS = vars(PARSER.parse_args())

    main(ARGS)
