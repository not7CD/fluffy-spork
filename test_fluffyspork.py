"""Testing module for fluffyspork"""

import unittest
import fluffyspork

test_paths = {'raw': 'test/raw',    'sorted': 'test/sorted'}
test_database = {'name': 'test-fluffyspork'}


class DataBase(unittest.TestCase):
    """docstring for DataBase."""

    def test_add_raw(self):
        """test_add_raw test automatic adding of files from raw folder"""
        pass


class ProcessDirectory(unittest.TestCase):
    """process_directory is a generator used to process all items in dir"""

    def test_recursive(self):
        """Print contents of test/"""
        def print_file(arg):
            print(arg)

        fluffyspork.process_directory(test_paths['raw'], print_file, True)

if __name__ == '__main__':
    unittest.main()
