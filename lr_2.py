import numpy
from PIL import Image
numpy.seterr(divide='ignore')


def find_ndvi(pic_b4, pic_b3):
    NIR = numpy.array(Image.open(pic_b4)).astype(int)
    R = numpy.array(Image.open(pic_b3)).astype(int)
    NDVI = (NIR - R) / (NIR + R)
    return NDVI


def drow_pic(ndvi):
    NDVI_pic = Image.new('RGB', (len(ndvi[0]), len(ndvi)), color=(255, 255, 255))
    inaccuracy = 0.12
    colors = {(-1., -0.): (4, 18, 60),
              (-0., 0.033): (252, 254, 252),
              (0.033, 0.066): (196, 184, 168),
              (0.066, 0.1): (178, 150, 107),
              (0.1, 0.133): (164, 130, 76),
              (0.133, 0.166): (143, 114, 71),
              (0.166, 0.2): (132, 154, 47),
              (0.2, 0.25): (148, 182, 20),
              (0.25, 0.3): (116, 170, 4),
              (0.3, 0.35): (100, 162, 4),
              (0.35, 0.4): (76, 146, 4),
              (0.4, 0.45): (60, 134, 4),
              (0.45, 0.5): (28, 114, 4),
              (0.5, 0.6): (4, 96, 4),
              (0.6, 0.7): (4, 73, 4),
              (0.7, 0.8): (4, 58, 4),
              (0.8, 0.9): (4, 41, 4),
              (0.9, 1 + inaccuracy): (4, 25, 4)}

    col, row = 0, 0
    for i in ndvi:
        for j in i:
            for interval in colors:
                if interval[0] - inaccuracy <= j < interval[1] - inaccuracy:
                    NDVI_pic.putpixel((col, row), colors[interval])
                    break
            col += 1
        col = 0
        row += 1
    return NDVI_pic


if __name__ == '__main__':
    b4_pic = 'cropped_krasnoyarsk_4.TIF'
    b3_pic = 'cropped_krasnoyarsk_3.TIF'
    pic = drow_pic(find_ndvi(b4_pic, b3_pic))
    pic.show()
