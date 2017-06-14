import re
from PIL import Image
import pytesseract
__version__ = '1.0.0'

def simple_tesseract(inpath, outpath=None, data=None, tags=None):
    img = Image.open(inpath)
    width, height = img.size
    img = img.crop((0, 0, width, int(height/2)))
    data = pytesseract.image_to_string(img, lang='pol')
    return {'data': data, 'path': inpath}

UNIT1_RE = re.compile(r'(organizacyjna\s{0,2}\W?)\s([\S\s]{0,200})?', re.IGNORECASE)
UNIT2_RE = re.compile(r'organizacyjna', re.IGNORECASE)

def simple_regexr(inpath=None, outpath=None, data=None, tags=None):
    result = UNIT1_RE.search(data)
    data = {}
    try:
        data['UNIT1_RE'] = str(result.group(0))
        # print(result.group(0))
        # input()
    except AttributeError as e:
        print(e)
    return {'data': data,'tags': ['test']}


def main():
    pass

if __name__ == '__main__':
    main()
