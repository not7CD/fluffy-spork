"""
    File: number-manualy.py
    Author: Norbert Szulc `not7CD`
    Open image and let user input its number manualy, then save it under new name in output directory.
"""

import argparse
import os
import re
import subprocess


from PIL import Image

# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg
# import numpy as np

PICTURE_RE = re.compile(r'.*\.jpg$', re.IGNORECASE)


def input_from_user(path):
    """Opens path with feh, waits for input from user"""
    feh = subprocess.Popen(['feh', path])
    # show massage in command line and ask for number shown in feh
    print("Input number from image:")
    number = input()
    feh.kill()
    return int(number)


def process_manualy(path):
    with Image.open(path) as img:
        width = img.size[0]
        img_tmp = img.crop((0, 0, width, width-300))
        img_tmp.save('tmp.jpg')
        return input_from_user('tmp.jpg')

def process_img(path, output_path, original_name):
    # """ This function rotates images to portrait rotation """
    # print("Opening image %s" % path)
    with Image.open(path) as img:
        width, height = img.size

        img_tmp = img.crop((0, 0, width, width-300))
        img_tmp.save('tmp.jpg')

        number = input_from_user('tmp.jpg')


        new_path = os.path.join(output_path, str(number) + '_' + original_name)
        print("Save to %s" % new_path)

        img.save(new_path)


def process_dir(path, output_path=None, recursive=False):
    """ Process all elements in directory, output processed in given output dir."""
    if not output_path:
        output_path = path

    if not os.path.isdir(path):
        print(path, 'is not a directory!')
    else:
        num_files = sum(os.path.isfile(os.path.join(path, f)) for f in os.listdir(path))
        file_num = 0

        for element in os.listdir(path):


            element_path = os.path.join(path, element)
            # element_output_path = os.path.join(output_path, element)

            if os.path.isdir(element_path) and recursive:
                process_dir(element_path, output_path, recursive)

            elif os.path.isfile(element_path) and re.match(PICTURE_RE, element_path):
                file_num += 1
                print("(%s/%s) %s," % (file_num, num_files, element))
                process_img(element_path, output_path, element)


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
