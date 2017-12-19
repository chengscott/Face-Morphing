#def resize(path1, path2)


im1 = Image.open("lif.png")
im2 = Image.open("imhs.jpg")

width = 500
height = 496

imr1 = im1.resize((width, height), Image.BILINEAR)
imr2 = im2.resize((width, height), Image.BILINEAR)

imr1.save("lifr.jpg")
imr2.save("imhsr.jpg")
