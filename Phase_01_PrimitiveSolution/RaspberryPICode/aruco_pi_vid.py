import cv2
import numpy as np


aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters_create()
font = cv2.FONT_HERSHEY_SIMPLEX
textCoordinates=(200,100)
# fontScale 
fontScale = 2
# Red color in BGR 
color = (0, 0, 255) 
# Line thickness of 2 px 
thickness = 2

def countArucoMarkedParkingSpaces(image,aruco_dict,aruco_params ):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)
    return len(ids)
	
vid = cv2.VideoCapture(0):
while(True):
	ret,frame=vid.read()
	free_spaces = countArucoMarkedParkingSpaces(frame,aruco_dict,aruco_params)
	cv2.putText(frame,"Free Spaces:{}".format(free_spaces),textCoordinates,font, fontScale,color,thickness,cv2.LINE_AA,False)
	cv2.imshow("Parking Status",frame)
	key = cv2.waitKey(1)
	if key == 27:
		break

vid.release()
cv2.destroyAllWindows()