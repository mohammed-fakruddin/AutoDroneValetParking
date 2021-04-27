# AutoDroneValetParking
## DGMD E-17 (26008) - Robotics, Autonomous Vehicles, Drones, and Artificial Intelligence

#### Team Members

* Ayush Bhasin
* Fakruddin Mohammed
* Mohammed Rahman

### Phase 1 - Primitive Parking Solution

* In this phase, the primitive parking solution just counts the number of parking space agailable.
* The phase-1 project makes the assumption that, the parking bays are painted with Aruco markers.
* Open CV library is used to count number of visible aruco markets (i.e. free parking spaces)


### Phase 1 Overview

![Project Overview](/Phase1_Overview.PNG)

### Code

* Step01_PrimitiveSolutionSimple - jupyter notebook has all the necessary code to run the phase-1 of the project

** It loads standard python, open-cv libraries
** It loads the aruco dictionary
** It reads the given image file of parking bays and counts the number of free parking spaces (i.e. visible aruco markers)
