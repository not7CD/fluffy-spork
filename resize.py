from PIL import Image
import numpy as np
import subprocess

def to_300dpi(path, output_path, data=None, tags=None):
    with Image.open(path) as img:
        size = np.array(img.size)
        print(size)
        size = size / (size[0] / 2400)
        print(size)
        img = img.resize(tuple(size.astype(int)), Image.BICUBIC)
        img.save(output_path)
    return data

def main():
    test_images = ['test/preprocess/rotate/P1380142.JPG', 'test/preprocess/rotate/IMG_6063.JPG']
    for path in test_images:
        to_300dpi(path, 'tmp.jpg')
        feh = subprocess.Popen(['feh', 'tmp.jpg'])
        input()
        feh.kill()

    # # time.sleep(3)
    # print(pytesseract.image_to_string(Image.open('tmp.jpg')))
    # print("PROCESSED WITH TESSERACT")


if __name__ == '__main__':
    main()
