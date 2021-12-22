import re
from PIL import Image


def find_coord_town():
    krasnoyarsk_coord = {'CORNER_UL_LAT_PRODUCT': 56.15572,  # широта
                         'CORNER_UL_LON_PRODUCT': 92.61526,
                         'CORNER_UR_LAT_PRODUCT': 56.15572,  # широта
                         'CORNER_UR_LON_PRODUCT': 93.20310,
                         'CORNER_LL_LAT_PRODUCT': 55.89637,
                         'CORNER_LL_LON_PRODUCT': 92.61526,
                         'CORNER_LR_LAT_PRODUCT': 55.89637,
                         'CORNER_LR_LON_PRODUCT': 93.20310}
    return krasnoyarsk_coord


def find_coord_pic(filename):
    coordinates = {}
    with open(filename, 'r') as f:
        for line in f:
            if re.search(r'CORNER_[UL][LR]_L[AO][TN]_PRODUCT', line):
                key_value = line.split(' = ')
                coordinates[key_value[0][4:]] = float(key_value[1][:-1])

    return coordinates


def find_town_rect(coord_town):
    return {'height': abs(coord_town['CORNER_UL_LAT_PRODUCT'] - coord_town['CORNER_LL_LAT_PRODUCT']),
            'width': abs(coord_town['CORNER_UL_LON_PRODUCT'] - coord_town['CORNER_UR_LON_PRODUCT'])}


def delta_pic_town_ul(coord_pic, coord_town):
    return {'height': abs(coord_pic['CORNER_UL_LAT_PRODUCT'] - coord_town['CORNER_UL_LAT_PRODUCT']),
            'width': abs(coord_pic['CORNER_UL_LON_PRODUCT'] - coord_town['CORNER_UL_LON_PRODUCT'])}


def find_town_pix_coord(rect_town, d_ul, pixel):
    left = d_ul['width'] * pixel['width']
    upper = d_ul['height'] * pixel['height']
    right = left + rect_town['width'] * pixel['width']
    lower = upper + rect_town['height'] * pixel['height']
    return {'left': left,
            'upper': upper,
            'right': right,
            'lower': lower}


def pixels_per_coordinate(filename, coordinates):
    image = Image.open(filename)
    image.crop()
    return {
            'width': abs(image.size[0] / (coordinates['CORNER_UL_LON_PRODUCT'] - coordinates['CORNER_UR_LON_PRODUCT'])),
            'height': abs(image.size[1] / (coordinates['CORNER_UL_LAT_PRODUCT'] - coordinates['CORNER_LL_LAT_PRODUCT']))
            }


def crop_pic(angles, filename_SR_B2):
    img = Image.open(filename_SR_B2)
    img_crop = img.crop((angles['left'], angles['upper'], angles['right'], angles['lower']))
    img_crop.save('cropped_krasnoyarsk.TIF')
    return img_crop


if __name__ == '__main__':
    MTL = "C:\\Users\\MI\\Desktop\\maёvnickek\\uchoba\\V\\ИС Аэрокосмических Комплексов\\" \
          "LE07_L1TP_142021_20020409_20200916_02_T1_MTL.txt"
    SR_B2 = "C:\\Users\\MI\\Desktop\\maёvnickek\\uchoba\\V\\ИС Аэрокосмических Комплексов\\" \
            "LE07_L1TP_142021_20020409_20200916_02_T1_B2.TIF"
    town_coord = find_coord_town()
    pic_coord = find_coord_pic(MTL)
    delta = delta_pic_town_ul(pic_coord, town_coord)
    pix = pixels_per_coordinate(SR_B2, pic_coord)
    town_rect = find_town_rect(town_coord)
    town_pix_coord = find_town_pix_coord(town_rect, delta, pix)
    crop_pic(town_pix_coord, SR_B2).show()
