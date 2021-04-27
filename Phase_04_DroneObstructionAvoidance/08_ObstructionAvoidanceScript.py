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
import random


stop_flag = False
DISTANCE_LIMIT = 400


img_width_original = 320
img_height_original = 240

img_height = 75
img_width = 75

origin = (25,25)
thickness = 2
fontScale=1

font = cv2.FONT_HERSHEY_SIMPLEX

def interrupt_drone_simple(tello, sig, frame):
    global stop_flag
    print('SIMPLE --> Taking control of drone for manual control')
    tello.send_rc_control(0, 0, 0, 0)
    stop_flag = True

    tello.land()
    tello.end()
    cv2.destroyAllWindows()
    print('Interrupted the drone')
    


def interrupt_drone_advanced(tello, sig, frame):
    global stop_flag
    print('ADVANCED -->Taking control of drone for manual control')
    tello.send_rc_control(0, 0, 0, 0)
    stop_flag = True
    #img = cv2.imread("picture.png")
    #cv2.imshow("PIC", img)
    #frame_read = tello.get_frame_read()
    #cv2.imshow("PIC", frame_read)
    while True:

        frame_read = tello.get_frame_read()
        cv2.imshow("PIC", frame_read.frame)
        key = cv2.waitKey(0) & 0xff
        if key == 27:
            break
        elif key == ord('w'):
            tello.move_forward(20)
            print('forward')
        elif key == ord('s'):
            tello.move_backward(20)
            print('backward')
        elif key == ord('a'):
            tello.move_left(20)
            print('left')
        elif key == ord('d'):
            tello.move_right(20)
            print('right')
    tello.land()
    #tello.end()
    cv2.destroyAllWindows()
    print('Interrupted the drone')


def initializeTello():
    myDrone = Tello()
    myDrone.connect()
    myDrone.for_back_velocity = 0
    myDrone. left_right_velocity = 0
    myDrone.up_down_velocity = 0
    myDrone.yaw_velocity = 0
    myDrone.speed = 0
    print('BATTERY LEVELS:', myDrone.get_battery())
    myDrone.streamoff()
    myDrone.streamon()
    return myDrone


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

def main():
    global stop_flag
    print('init drone')
    myDrone = initializeTello()
    print('load model')
    loaded_model = load_obstruction_avoidance_model()
    print('link interrupts for manual control')
    signal.signal(signal.SIGINT, partial(interrupt_drone_advanced, myDrone))
    signal.signal(signal.SIGBREAK, partial(interrupt_drone_simple, myDrone))
    
    total_distance_moved = 0

    # take of the drone
    myDrone.takeoff()
    
    while not stop_flag:
        print("total distance travelled so far... {}cm ".format(total_distance_moved))
        frame_read = myDrone.get_frame_read()
        image = frame_read.frame
        

        #2. Take a copy of the image and resize
        image_copy = image.copy()
        image_copy2 = cv2.resize(
            image_copy, (img_width_original, img_height_original))

        
        #3. Define the vertices for ROI
        vertices = np.array([[(img_width_original*1/3, 0),
                              (1/3*img_width_original, img_height_original*1/2),
                              (2/3*img_width_original, 1/2*img_height_original),
                              (2/3*img_width_original, 0)]], dtype=np.int32)

        masked_image = region_of_interest(image_copy2, vertices)
        masked_image_copy = masked_image.copy()
        #4. Resize the masked image for input to the model
        masked_image = cv2.resize(masked_image, (img_height, img_width))
        masked_image = masked_image.reshape(1, img_width, img_height, 3)
        status = loaded_model.predict(masked_image)

        print('Model Prediction-1: ', status)
        direction=""
        color = (255,0,0)
        if status[0][0] < 0.5:
            direction="NO obstruction"
            print('DIRECTION:', direction)
            if not stop_flag:
                myDrone.move_forward(20)
                total_distance_moved = total_distance_moved + 20
        else:
            # If obstruction, move - left
            # and check if there is obstruction in left too
            # if so, move right
            color = (0, 0, 255)
            direction = "Obstruction - move left"
            print('DIRECTION:', direction)
            if not stop_flag:
                if random.randint(0,1) ==0:
                    myDrone.move_left(20)
                else:
                    myDrone.move_right(20)
                total_distance_moved = total_distance_moved + 10
            
            # after moving left, check if there is a obstruction
            # if so, move right
            frame_read = myDrone.get_frame_read()
            image = frame_read.frame
            #2. Take a copy of the image and resize
            image_copy = image.copy()
            image_copy2 = cv2.resize(
                image_copy, (img_width_original, img_height_original))
            #3. Define the vertices for ROI
            
            masked_image = region_of_interest(image_copy2, vertices)
            masked_image_copy = masked_image.copy()
            
            #4. Resize the masked image for input to the model
            masked_image = cv2.resize(masked_image, (img_height, img_width))
            masked_image = masked_image.reshape(1, img_width, img_height, 3)
            status = loaded_model.predict(masked_image)
            
            if status[0][0] > 0.5:
                direction = "Obstruction - move right"
                print('DIRECTION:', direction)
                if not stop_flag:
                    myDrone.move_right(20)
                    total_distance_moved = total_distance_moved + 20

        cv2.putText(image_copy2,direction,origin, font,fontScale,color,thickness,cv2.LINE_AA)
        cv2.imshow("Main", image_copy2)
        cv2.imshow("Masked", masked_image_copy)
        key = cv2.waitKey(1)
        if key == 27:
            break
        if total_distance_moved >= DISTANCE_LIMIT:
            print("*************** LANDING **************")
            print("total travelled distance {}cm exceeded, so landing".format(total_distance_moved))
            print("*************** LANDING **************")
            stop_flag = True
            myDrone.land()
            #myDrone.end()
            cv2.destroyAllWindows()
        

    myDrone.land()
    #myDrone.end()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    main()
