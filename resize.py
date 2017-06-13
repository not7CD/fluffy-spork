from PIL import Image
import numpy as np
# import timeit from timeit

def resize_300dpi(path, output_path, data=None, tags=None):
    with Image.open(path) as img:
        size = np.array(img.size)
        # print(size)
        size = size / (size[0] / 2400)
        new_size = tuple(size.astype(int))
        # print(size)
        if img.size[0] != new_size[0]:
            img = img.resize(new_size, Image.BICUBIC)

        img.save(output_path)
    return img.size

def main():
    import subprocess
    import pytesseract
    import cleanimage
    test_images = ['test/preprocess/rotate/P1380142.JPG', 'test/preprocess/rotate/IMG_6063.JPG']
    for path in test_images:
        resize_300dpi(path, 'tmp.jpg')
        cleanimage.imagemagic_textcleaner('tmp.jpg', 'tmp2.jpg')
        feh = subprocess.Popen(['feh', 'tmp2.jpg'])
        print(pytesseract.image_to_string(Image.open('tmp2.jpg')))
        print("PROCESSED WITH TESSERACT")
        input()
        feh.kill()

    # # time.sleep(3)


if __name__ == '__main__':
    main()
