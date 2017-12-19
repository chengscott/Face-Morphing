from PIL import Image

def resize(path, name):
    im1 = Image.open(path)

    width = 500
    height = 496

    imr1 = im1.resize((width, height), Image.BILINEAR)

    imr1.save(name)
