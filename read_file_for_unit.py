"""Zczytywanie danych z plików i ich Sortowanie"""

try:
    import Image
except ImportError:
    from PIL import Image

import pytesseract

print(pytesseract.image_to_string(Image.open('data/test_data/test2.jpg'), lang='pol'))
