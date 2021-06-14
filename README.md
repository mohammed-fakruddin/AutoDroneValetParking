# AutoDroneValetParking
## DGMD E-17 (26008) - Robotics, Autonomous Vehicles, Drones, and Artificial Intelligence



### Current Issues

* Parking Grid Technology (a student start-up company which went burst) adopted IOT sensor approached to find the open parking space, publish it to smart mobile app to guide the people looking for parking space.
* Installation of IOT sensor in each parking space needs huge initial capital, complex operation and overhead of maintaining the IOT sensors.



### Motivation

* Therefore, the motivation for this project is to leverage the technology to find cost effective solution and COVID compliant safe parking.



### Project Objectives

**Using technology improve the user experience of parking at busier places addressing the following issues:**

* Bring savings by replacing valet parking with drone assisted parking
* COVID Free parking
* Cost effective phased implementation approach




### Project Overview

![Project Overview](/images/overview.PNG)

### Project Phases

* Phase 1 - Primitive Solution using Open CV and Aruco Markers
* Phase 2 & 3 - Open CV Image Segmentation of Car Parking Bays and CNN Classification Model for Car Parking Status
* Phase 4 - Drone Obstruction Avoidance Model
* Phase 5 - Autonomous Path Navigation using Djikstra Algorithm

### Project Presentation Slides

https://drive.google.com/file/d/1t1aS51OR4CDeDXFmVReShamhZEW4xQaH/view?usp=sharing


### Project Video

https://drive.google.com/file/d/1aVUqnjvBrmsQksUnqUX703CRoJIdiEHA/view?usp=sharing


### Datasets

#### Car Parking Bays Image Segmentation Dataset
https://drive.google.com/file/d/1zDV8ZjRgaNVB6SExCJ-nEo2WcF_kyiZo/view?usp=sharing

#### Obstruction avoidance images dataset
https://drive.google.com/file/d/1EuXFDl4uz8ikPuVodC7wDUzpjErE9mmJ/view?usp=sharing

## Hardware Requirements
1. DJI Tello
2. Raspberry PI
3. PI Camera or Webcam

## Software Requirements and Installation Instruction
The following python libraries are used to implement the project. These libraries can be installed using the "pip install" command.
* Open CV (Version 4.2)
* Tensorflow (V2.1)
* Tensorflow Lite (V2.1)
* Scikit-learn (latest version)
* Numpy/Scipy (latest version)
* Pandas (latest version)
* DJITello (Latest version)

### Issues & Challenges
* Parking Bays image segmentation using Open CV is sensitive to lighting conditions
* Outdoor testing using Tello drone which weights approximately 80g is challenging due to heavy winds. Therefore, outdoor testing is avoided and resorted back to indoor and hence re-do the obstruction avoidance avoiding indoor objects



### Conclusions
* Overall end-to-end concept of phased implementation for COVID Free Drone Auto Valet Parking is implemented
* Working prototype using Tello drone, toy card and other house hold objects is successfully built



### Future Work

* Test the model outdoor in real parking space
* Collect more outdoor obstruction images and improve the model efficiency
* Optimise the computational pipeline for obstruction avoidance and path planning


