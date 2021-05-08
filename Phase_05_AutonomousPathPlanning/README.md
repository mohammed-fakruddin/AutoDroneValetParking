# Code

1. **10_DronePathPlanningDjikstra.py:** This is the core python script file which performs the following steps:

* Buils UI for Djikstra path planning with start and target node
* The code finds path and builds a drone navigation route
* Once the drone navigation route is worked out using the Djikstra algorithm, the following code snippet sends flying instructions to the DJI Tello drone
```
for direction in heading:
        print('flying to:', direction)
        frame_read = myDrone.get_frame_read()
        image = frame_read.frame
        image = cv2.resize(image, (img_width_original, img_height_original))

        if direction == 'north': 
            #if prev direction is west - clockwise
            #if prev direction is east - counter clockwise
            if prev_direction == 'west':
                myDrone.rotate_clockwise(90)
            elif prev_direction == 'east': #east
                myDrone.rotate_counter_clockwise(90)
            myDrone.move_forward(25)
           
        elif direction == 'east':
            #if prev direction is north - clockwise
            #if prev direction is south - counter clockwise
            if (prev_direction == 'north'):
                myDrone.rotate_clockwise(90)
            elif(prev_direction == 'south'):
                myDrone.rotate_counter_clockwise(90)
            myDrone.move_forward(25)
                    
        elif (direction == 'west'):
            #if prev direction is north - counter clockwise
            #if prev direction is south - clockwise
            if (prev_direction == 'north'):
                myDrone.rotate_counter_clockwise(90)
            elif (prev_direction == 'south'):
                myDrone.rotate_clockwise(90)
            myDrone.move_forward(25)
        
        elif direction == 'south':
            #if prev direction is east - clockwise
            #if prev direction is south - counter clockwise
            if (prev_direction == 'west'):
                myDrone.rotate_counter_clockwise(90)
            elif (prev_direction == 'east'):
                myDrone.rotate_clockwise(90)
            myDrone.move_forward(25)
 ```
