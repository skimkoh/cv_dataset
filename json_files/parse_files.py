import numpy as np
from PIL import Image, ImageDraw
import json
import math
import glob
import os
import sys

def parse_shape(shape, size):
    '''
    Using https://stackoverflow.com/questions/3654289/scipy-create-2d-polygon-mask
    Inputs:
    shape: dictionary that states type of shape, and the border
    size: tuple of size of the original image of the shape
    '''
    #mask = np.zeros(size, dtype=bool)
    img = Image.new('1', size, 0)
    polygon_type = shape['name']

    if polygon_type == 'circle':
        cx, cy, r = shape['cx'], shape['cy'], shape['r']
        xy = [cx-r, cy-r, cx+r, cy+r]
        ImageDraw.Draw(img).ellipse(xy, fill=1, outline=1)

    if polygon_type == 'ellipse':
        #draw ellipse
        img_ = img.copy()
        cx, cy, rx, ry, theta = shape['cx'], shape['cy'], shape['rx'], shape['ry'], shape['theta'] 
        xy = [cx-rx, cy-ry, cx+rx, cy+ry]
        ImageDraw.Draw(img_).ellipse(xy, fill=1, outline=1)
        img_ = img_.rotate(-math.degrees(theta), center=(cx, cy))

        #rotate ellipse
        l = rx if rx>ry else ry
        box = (math.floor(cx-l), math.floor(cy-l),math.ceil(cx+l),math.ceil(cy+l))
        cropped = img_.crop(box)

        #paste ellipse
        Image.Image.paste(img, cropped, (math.floor(cx-l), math.floor(cy-l))) 
        

    if polygon_type == 'polyline' or polygon_type == 'polygon':
        x, y = shape['all_points_x'], shape['all_points_y']
        xy = list(zip(x,y))
        ImageDraw.Draw(img).polygon(xy, fill=1, outline=1)

    if polygon_type == 'rect':
        x, y, w, h = shape['x'], shape['y'], shape['width'], shape['height']
        xy = [x, y, x+w, y+h]
        ImageDraw.Draw(img).rectangle(xy, fill=1, outline=1)

    return img

ROOT_DIR = os.path.abspath("../../")
json_path = os.path.join(ROOT_DIR, '/content/cv_dataset/json_files')
mask_path = os.path.join(ROOT_DIR, '/content/cv_dataset/mask_arrs')
img_path = os.path.join(ROOT_DIR, '/content/cv_dataset/JPEGImages')

#json_path = "C:/Users/User/Desktop/Computer Vision/cv_dataset/cv_dataset/json_files"
#mask_path = "C:/Users/User/Desktop/Computer Vision/cv_dataset/cv_dataset/mask_arrs"
#img_path = "C:/Users/User/Desktop/Computer Vision/cv_dataset/cv_dataset/JPEGImages"

class_ids = ['BG', 'apple', 'orange', 'plum', 'banana', 'lemon', 'sachima',
                 'bread', 'peach', 'qiwi', 'tomato', 'grape', 'egg', 'litchi',
                 'bun', 'doughnut', 'fired_dough_twist', 'mango', 'mooncake', 
                 'pear', 'coin']

for idx, file in enumerate(glob.glob(os.path.join(json_path, '*.json'))):
    with open(file) as json_file:
        data = json.load(json_file)
    for key in data.keys():
        sample = key.split('.')[0]
        regions = data[key]['regions']
        if len(regions) == 0:
            print("{} has no regions recorded".format(sample))
        if regions != []:
            with Image.open(os.path.join(img_path, "{}.JPG".format(sample))) as img:
                size = img.size
                arr = np.zeros((img.size[1], img.size[0], 0), dtype=bool)
                attributes = []
                if len(regions) >= 2:
                    for idx, region in enumerate(regions):
                        if idx < 2: # I encountered repeat data
                            try:
                                attribute = region['region_attributes']['Attribute']
                            except:
                                attribute = region['region_attributes']['item']
                            attributes.append(class_ids.index(attribute))
                            shape = region['shape_attributes']
                            img = parse_shape(shape, size)
                            arr = np.concatenate((arr, np.array(img)[:,:,None]), axis=2)
                        else:
                            print("{} has {} regions recorded".format(sample, len(regions)))
                            break
                    if attributes.count(20) == 1:
                        np.save(os.path.join(mask_path, '{}_mask.npy'.format(sample)), arr)
                        np.save(os.path.join(mask_path, '{}_mask_class.npy'.format(sample)), np.array(attributes, dtype=int))
                    else:
                        print("did not find exactly 1 coin mask for {}".format(sample))
                else:
                    print("{} has < 2 regions recorded".format(sample))
