import signal
import sys
import time

from djitellopy import Tello
import cv2
import pygame
from functools import partial

import tensorflow as tf
import tensorflow.keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.models import model_from_json

import numpy as np

img_width_original = 320
img_height_original = 240

img_height = 75
img_width = 75

origin = (25, 25)
thickness = 1
fontScale = 1

font = cv2.FONT_HERSHEY_SIMPLEX



def load_obstruction_avoidance_model(model_json='drone_obstruction_model.json',
                                     model_weights='drone_obstruction_model.h5'):
    # load json and create model
    json_file = open(model_json, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_weights)
    print("Loaded model from disk")
    # evaluate loaded model on test data
    loaded_model.compile(loss='binary_crossentropy',
                         optimizer='adam', metrics=['accuracy'])
    return loaded_model


def region_of_interest(img, vertices):
    """
    Applies an image mask.
    
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    `vertices` should be a numpy array of integer points.
    """
    #defining a blank mask to start with
    mask = np.zeros_like(img)

    #defining a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]  # i.e. 3 or 4 depending on your image
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    #filling pixels inside the polygon defined by "vertices" with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    #returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image


loaded_model = load_obstruction_avoidance_model()
#vidcap = cv2.VideoCapture("1616842861616.mp4")
vidcap = cv2.VideoCapture("1616847434370.mp4")
success, image = vidcap.read()
count = 0
success = True
while success:
    #1. Get the image
    success, image = vidcap.read()
    
    #2. Take a copy of the image and resize
    image_copy = image.copy()
    image_copy2 = cv2.resize(
        image_copy, (img_width_original, img_height_original))
    #3. Define the vertices for ROI
    vertices = np.array([[(img_width_original*1/3, 0),
                (1/3*img_width_original, img_height_original*1/2), 
                (2/3*img_width_original, 1/2*img_height_original),
                (2/3*img_width_original, 0)]], dtype = np.int32)

    masked_image = region_of_interest(image_copy2,vertices)

    #4. Take a copy of masked image and show
    masked_image_copy = masked_image.copy()
    cv2.imshow("Masked", masked_image_copy)

    #5. Resize the masked image for input to model
    masked_image = cv2.resize(masked_image,(img_width,img_height))
    masked_image = masked_image.reshape(1, img_width, img_height, 3)
    
    #5. Get model prediction

    status = loaded_model.predict(masked_image)
    print('Model Prediction-1: ', status)
    
    direction = ""
    color = (0, 255, 0)
    
    if status[0][0] < 0.5:
        direction = "NO obstruction"
        print('DIRECTION:', direction)
    else:
        color = (0, 0, 255)
        direction = "YES obstruction"

    cv2.putText(image_copy2, direction, origin, font,
                        fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow("Main", image_copy2)

    key = cv2.waitKey(1)
    if key == 27:
        break

cv2.destroyAllWindows()

  
