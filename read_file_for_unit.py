"""Zczytywanie danych z plików i ich Sortowanie"""

try:
    import Image
except ImportError:
    from PIL import Image
import pytesseract

print(pytesseract.image_to_string(Image.open('data/raw_data/P1380061.JPG'), lang='pol'))
