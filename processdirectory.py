"""Iterate thru given directories?"""

import os
import re

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
