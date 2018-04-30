# Portfolio
Projects before I started using github, look around and use it freely, Be aware these are from the dark times I did not yet commented my code properly and coded without any regard for clarity :D 
I made most of these projects in my free time, but used them sometimes for hand ins. I only included the more interesting projects of the last 3 years.

## The Symulation of the Influenza Virus Spread: 
Labview symulation of the population dynamics effect of a flu epidemic. Won 2nd price at the BUTE student association competition. It was written in Labview 2018. The project file with all dependencies can be find in the folder, with the complete documentation in Hungarian.
Video: https://www.youtube.com/watch?v=vES5bmKey6E

## User Identification Based on Typing Patterns:
Created a classifier for identification based on typing, used feature based machine learning methods with Scikit Learn. Achieved 97% accuracy. Won the inhouse challange during the Data Mining class. The data was recorded from several users trough a javascript client, the data was provided to me by a professor. The classifier is based on trnsforming the data to features with Dinamic Time Warping. I fitted several types of classifiers, but later decided to use only knn as a base algorithm. I used knn inside a semisupervised algorithm I created, to get from 84% accuracy to 97%. 

## Analyze and use the ASPICE system development process: 
Bachelor thesis written at Bosch GMBH. I have created a system for database monitoring in DXL and python language. The system would go trough the requirement database, and if it found errors or missing information would send emails and statistics directly to the file owners. Performed also the system architecture planning for the computer responsible for car ignition. Here only the documentation is available, the code falls under NDA.

## PBD++ 
a program for making programming by demonstration easier with the Baxter robot, It helps the user by infering intent and automatically opening closing the grippers during demonstration. Uses rospy, kinect sensor and the Baxter robot.

## Baxter Speech Interface: 
Created a a voice interface for the Baxter robot, based on Google Speech Api, Api.ai, IBM Watson TTS. Users can interact with Baxter trough voice. Robot can perform online queries, start teaching by demonstration, do simple movements etc. The interesting thing is that it is possible to perform programming-by-demonstration trough voice commands, and api.ai gets refreshed too by the new commands dynamically. (Wrote the whole thing also with wit.ai, but the performance is much worse)

Video: https://www.youtube.com/watch?v=dMY-XXwBIb8


## Development of an Augmented Reality Engine Based on Real-time Object Detection
The project is based on the DarkNet framework. I have collected a dataset and trained a YOLO2 classifier. The application relies on heavy parallel computations and asyncronous threads. Also implemented an anomaly detection algorithm from a recent paper for more reliability.

Video: https://www.youtube.com/watch?v=RY7PWVt2vWE

## Turtlebot Soccer: 
Programmed two turtlebot robots to be able to pass a ball and score a goal. Wrote this project with Yu Sin Lin for Cooperative Robotics subject. The turtlebots are programmed in rospy. They use odometry and rgb-d cameras as sensors. The interesting part is that the image preprocessing is really slow and noisy, for this reason we used several tricks for sensor filtering and calibration. For filtering we applied hierarchical clustering.

## Grasping Characterization by using Symmetry Knowledge: 
A program for grasping object with the Baxter robot. Relies on MaskRCNN for instance segmentation, from the MatterPort repository. For inverse kinematics it uses the Baxter IKService.








