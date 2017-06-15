import re
from PIL import Image
import pytesseract
__version__ = '1.0.0'


def simple_tesseract(inpath, outpath=None, data=None, tags=None):
    img = Image.open(inpath)
    width, height = img.size
    img = img.crop((0, 0, width, int(height / 2)))
    data = pytesseract.image_to_string(img, lang='pol')
    return {'data': data, 'path': inpath}

RE_LIST = [
    ('UNIT1_RE', re.compile(
        r'(organizacyjna\s{0,2}\W?)\s([\S\s]{0,200})?', re.IGNORECASE)),
    ('UNIT2_RE', re.compile(
        r'(\wrg\wn\wz\wc\wjn\w\s{0,2}\W?)\s([\S\s]{0,200})?', re.IGNORECASE)),
    ('UNIT4_RE', re.compile(
        r'(pr\wz\wc\wjn\w\s{0,2}\W?)\s([\S\s]{0,200})?', re.IGNORECASE)),
    ('UNIT3_RE', re.compile(
        r'(K\wt\wd\wr\w\s{0,2})([\S\s]{0,100})?', re.IGNORECASE))
]


def simple_regexr(inpath=None, outpath=None, data=None, tags=None):
    results = {}
    for name, expr in RE_LIST:
        result = expr.search(data)
        try:
            results[name] = str(result.group(0))
        except AttributeError as e:
            print(e)

    return {'data': results, 'tags': ['test']}


def main():
    pass

if __name__ == '__main__':
    main()
