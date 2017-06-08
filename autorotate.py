#!/usr/bin/env python

from __future__ import print_function

"""
File: autorotate.py
Origial Author: Damien Riquet <d.riquet@gmail.com>
Current Maintainer: Trinh Nguyen <dangtrinhnt[at]gmail[dot]com>
Description: This script provides an auto-rotate feature of pictures

USAGE: autorotate.py [-h] [--recursive] directory [directory ...]

positional arguments:
  directory

optional arguments:
  -h, --help       show this help message and exit
  --recursive, -r
"""

import os
import re
import argparse
from PIL import Image

# this will help you bypass the truncated images
# the truncated images will be completed to full size with gray color.
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True


picture_re = re.compile(r'.*\.jpg$', re.IGNORECASE)


def autorotate(path):
    """ This function autorotates a picture """
    image = Image.open(path)
    try:
        exif = image._getexif()
    except AttributeError as e:
        print("Could not get exif - Bad image!")
        return False

    (width, height) = image.size
    # print "\n===Width x Heigh: %s x %s" % (width, height)
    if not exif:
        if width > height:
            image = image.rotate(90)
            image.save(path, quality=100)
            return True
    else:
        orientation_key = 274  # cf ExifTags
        if orientation_key in exif:
            orientation = exif[orientation_key]
            print(orientation)
            rotate_values = {
                3: 180,
                6: 270,
                8: 90
            }
            if orientation in rotate_values:
                # Rotate and save the picture
                image = image.rotate(rotate_values[orientation])
                image.save(path, quality=100, exif=str(exif))
                return True
        else:
            if width > height:
                image = image.rotate(90)
                image.save(path, quality=100, exif=str(exif))
                return True

    return False

# new_width = 200
# new_height = 300


def autoresize(path, new_width, new_height):
    image = Image.open(path)
    (width, height) = image.size
    if width < height:
        if width != new_width and height != new_height:
            image = image.resize((new_width, new_height), Image.ANTIALIAS)
            image.save(path, quality=100)
            return True

    return False


def process_directory(path, recursive=False, new_width=None, new_height=None):
    """ This function processes all elements from a directory """

    print("\n==new_width: %s\n" % new_width)
    print("\n==new_height: %s\n" % new_height)

    if not os.path.isdir(path):
        print(path, 'is not a directory')

    else:
        for elt in os.listdir(path):
            elt_path = os.path.join(path, elt)
            if os.path.isdir(elt_path) and recursive:
                process_directory(elt_path, recursive)

            elif os.path.isfile(elt_path) and re.match(picture_re, elt_path):
                print("=== Processing %s ===" % (elt))
                for i in range(1):  # for some reason, I have to do it twice
                    if autorotate(elt_path):
                        print('autorotate: %s/%s' % (path, elt))
                if new_width and new_height:
                    if autoresize(elt_path, new_width, new_height):
                        print('autoresize: %s/%s' % (path, elt))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dir', '-d', nargs='+')
    parser.add_argument('--output-dir', '-o', nargs='+')
    parser.add_argument('--recursive', '-r', action='store_true')
    parser.add_argument('--resize', nargs='+')
    args = parser.parse_args()

    width = None
    height = None
    if args.resize:
        if len(args.resize) == 2:
            width = int(args.resize[0])
            height = int(args.resize[1])

    for d in args.dir:
        process_directory(d, args.recursive, width, height)
