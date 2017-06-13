import subprocess
from PIL import Image
import pytesseract


def imagemagic_textcleaner(inpath, outpath, data=None, tags=None):
    args = [
        '-g',
        '-e', 'stretch',
        '-f', '25',
        '-o', '10',
        '-t', '30',
        '-u',
        '-s', '1',
        '-T',
        '-p', '5']
    subprocess.check_call(['./textcleaner',
                           '-g',
                           '-e', 'stretch',
                           '-f', '25',
                           '-o', '10',
                           '-t', '30',
                           '-u',
                           '-s', '1',
                           '-T',
                           '-p', '5', inpath, outpath])
    return args


def main():
    imagemagic_textcleaner('test/preprocess/rotate/IMG_6063.JPG', 'tmp.jpg')
    # # time.sleep(3)
    feh = subprocess.Popen(['feh', 'tmp.jpg'])
    print(pytesseract.image_to_string(Image.open('tmp.jpg')))
    print("PROCESSED WITH TESSERACT")

    input()
    feh.kill()
    # feh = subprocess.Popen(['feh', 'test/preprocess/rotate/P1380098.JPG'])

if __name__ == '__main__':
    main()
