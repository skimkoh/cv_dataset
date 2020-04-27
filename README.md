# 50.035 Computer Vision
### Estimating calories using computer vision

To estimate calories of a food, we need to detect the object and estimate the volume, from which we can use standardized nutritional information to get the calories of the object. 

#### Object Detection

We tried 3 models for object detection, namely naive CNN, Faster R-CNN and Mask R-CNN. 

Accuracy: 

1. CNN - 60%      (label only)
2. FRCNN - 90.9%  (label only) 
3. MRCNN - 94.75% (mAP) 

#### Volume Estimation

It uses the image segmentation from MRCNN to calculate the volume via the mask. We get the normalized food pixel area by the ratio of the calibration object, the yuan coin. Through this way, we can get the average volume per pixel for each food, which we will multiple with the extracted normalized area from masks from test images to get the predicted volume. 

Our results shows an average of +-9.8% deviation of food volume across the dataset of 19 classes.
