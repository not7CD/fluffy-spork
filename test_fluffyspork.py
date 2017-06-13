"""Testing module for fluffyspork"""

import unittest
import rotate

test_paths = {'raw': 'test/raw',    'sorted': 'test/sorted'}
test_database = {'name': 'test-fluffyspork'}


class RotateKnownValues(unittest.TestCase):
    """test rotate.py."""
    known_values = [
        ([200, 300], None, 0),
        ([400, 300], None, 90),
        ([200, 300], {'flip':None}, 180),
        ([400, 300], {'flip':None}, 270)
        ]
    def test_determine_rotation(self):
        """test_add_raw test automatic adding of files from raw folder"""
        for size, tags, expected in self.known_values:
            actual = rotate.determine_rotation(size, tags)
            self.assertEqual(expected, actual, 'Wrong rotation')


if __name__ == '__main__':
    unittest.main()
