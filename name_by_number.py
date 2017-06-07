"""Zczytywanie danych z plików i ich Sortowanie"""

try:
    import Image
except ImportError:
    from PIL import Image

# import pytesseract

if __name__ == '__main__':
    im = Image.open('data/test_data/test.jpg')
    im.show()
