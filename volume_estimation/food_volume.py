# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 14:03:54 2020

@author: BAI JIALONG
"""

import numpy as np
import pandas as pd
from PIL import Image
import cv2


food_vol_train = pd.read_csv("food_volume_train.csv")
food_vol_train = food_vol_train.to_numpy()

##Load the mask of the food and the coin
food_mask = np.load("train/food_masks.npy")
coin_mask = np.load("train/coin_masks.npy")

#load the corresponding filename for the food and coin mask
f = open("train/ftood_masks_filename.txt", "r")
mask_name =f.read()
f.close()
food_mask_type = [i[:i.find("(")-4] for i in mask_name.split("\n")]
#print(food_mask_type)
food_set=set(food_mask_type)
#print(food_set)

#load actual food volume
f = open("train/food_vol_actual.txt", "r")
vol_list =f.read()
f.close()
food_vol = [int(i) for i in vol_list.split("\n")]
#print(food_vol)

w, h, idx = food_mask.shape

#initalise training & error database
food_pixels={}
for i in food_set:
    food_pixels[i]=[]
food_error={}
for i in food_set:
    food_error[i]=[]
#print (food_pixels)

#Determine the diameter of the coin
for i in range(idx-1):
    this_food = food_mask_type[i]
    this_volume = food_vol[i]
    surface_area = np.count_nonzero(food_mask[:,:,i]==1)
    c_coin_mask = coin_mask[:,:,i].astype(np.uint8)
    coin_area = np.count_nonzero(c_coin_mask==1)
    
    #finding the radius of coin
    contours, _ = cv2.findContours(c_coin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for j, c in enumerate(contours):
        contours_poly[j] = cv2.approxPolyDP(c, 3, True)
        boundRect[j] = cv2.boundingRect(contours_poly[j])
        centers[j], radius[j] = cv2.minEnclosingCircle(contours_poly[j])
    
#    #Saving the mask as an image output
#    im = Image.fromarray(np.uint8(food_mask[:,:,i])*255)
#    im.save("image/food{}{}.png".format(i,this_food))
#    im2 = Image.fromarray(np.uint8(coin_mask[:,:,i+1])*255)
#    im2.save("image/coin{}{}.png".format(i,this_food))
    
    #Diameter of coin
    diameter = radius[0]*2
    norm_coeff = 25/(diameter)
    
    #normalise the surface area
    norm_area = surface_area*norm_coeff
    
    #calculate the volume/pixel
    vol_per_pixel = this_volume/norm_area
    
    #storing norm_area
    food_pixels[this_food].append(vol_per_pixel)
    
#average food pixels (This is the trained model)
avg_food_pixels = {}
for key, value in food_pixels.items():
    avg= sum(value)/max(len(value),1)
    avg_food_pixels[key]=avg
print(avg_food_pixels)
    
#importing test model

## Modified for testing orange
food_mask = np.load("test/IMG_20200423_144851.npy")[0]
coin_mask = np.load("test/IMG_20200423_144851.npy")[1]

w, h, idx = food_mask.shape

#Testing: Estimating the food volume
for i in range(idx-1):
    this_food = food_mask_type[i]
    this_volume = food_vol[i]
    surface_area = np.count_nonzero(food_mask[:,:,i]==1)
    c_coin_mask = coin_mask[:,:,i].astype(np.uint8)
    coin_area = np.count_nonzero(c_coin_mask==1)
    
    #finding the radius of coin
    contours, _ = cv2.findContours(c_coin_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours_poly = [None]*len(contours)
    boundRect = [None]*len(contours)
    centers = [None]*len(contours)
    radius = [None]*len(contours)
    for j, c in enumerate(contours):
        contours_poly[j] = cv2.approxPolyDP(c, 3, True)
        boundRect[j] = cv2.boundingRect(contours_poly[j])
        centers[j], radius[j] = cv2.minEnclosingCircle(contours_poly[j])
    
    #Saving the mask as an image output
    im = Image.fromarray(np.uint8(food_mask[:,:,i])*255)
    im.save("image/food{}{}.png".format(i,this_food))
    im2 = Image.fromarray(np.uint8(coin_mask[:,:,i+1])*255)
    im2.save("image/coin{}{}.png".format(i,this_food))
    
    #Diameter of coin
    diameter = radius[0]*2
    norm_coeff = 25/(diameter)
    
    #normalise the surface area
    norm_area = surface_area*norm_coeff
    
    #get data from model
    vol_coeff = avg_food_pixels[this_food]
    
    #calculate the volume
    est_volume = norm_area*vol_coeff
    error = (est_volume-this_volume)/this_volume
    
    #storing error
    food_error[this_food].append(error)
    
#average food error (Result of the test)
avg_food_error = {}
for key, value in food_error.items():
    avg= sum(value)/max(len(value),1)
    avg_food_error[key]=avg
print(avg_food_error)