# 50.035 Computer Vision
### Estimating calories using computer vision

To estimate calories of a food, we need to detect the object and estimate the volume, from which we can use standardized nutritional information to get the calories of the object. 

#### Object Detection

We tried 3 models for object detection, namely naive CNN, Faster R-CNN and Mask R-CNN. 

Accuracy: 

1. CNN - 60%      (label only)
2. FRCNN - 90.9%  (label only) 
3. MRCNN - 94.75% (label),  98% (mAP) 

#### CNN 
Simple CNN. Model includes 2D convolutional layers, max pooling, dense and softmax layers. The weights of the model are classifier.h5 and classifier.json.
  
#### FRCNN 
Consists of two .ipynb files. frcnn_train.ipynb is used for training and frcnn_test.ipynb is used for testing, which will produce the results and confusion matrix. Code is found in another git repo at https://github.com/skimkoh/cv_keras. To test the model, you can download the weights via the dropbox link. 

FRCNN is not sufficient enough for our needs for the later volume estimation. Therefore, we tried using MRCNN.

#### MRCNN
The .ipynb is located in the mrcnn folder, and weights are located in the dropbox link at the bottom. MRCNN is able to produce a mask of the fruit in the picture. 
  
#### Volume Estimation

It uses the image segmentation from MRCNN to calculate the volume via the mask. We get the normalized food pixel area by the ratio of the calibration object, the yuan coin. Through this way, we can get the average volume per pixel for each food, which we will multiple with the extracted normalized area from masks from test images to get the predicted volume. 

Our results shows an average of +-9.8% deviation of food volume across the dataset of 19 classes. 

The file can be located in the volume_estimation folder. Arrays of masks used are located in the dropbox link below. 

#### Other links

Dropbox link (for model weights, array of masks, etc): https://www.dropbox.com/sh/lm5gsmvvhyf2lrx/AABuwHcD8YRgxVdO_zSopQ-Va?dl=0


FRCNN model (mentioned for FRCNN): https://github.com/skimkoh/cv_keras
