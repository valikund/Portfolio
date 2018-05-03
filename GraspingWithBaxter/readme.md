# Grasping Characterization by using Symmetry Knowledge:

A program for grasping object with the Baxter robot. Relies on MaskRCNN for instance segmentation, from the MatterPort repository. For inverse kinematics it uses the Baxter IKService. The program segments the objects to the pixel level. Then calculates the center point and the first and second axis of inertia. If the object is symmetric the first axis is the moirror axis, so the object has to be picked with a parallel gripper parallel to the second axis, above the center of mass. From the 2D object localizes the 2 grapsing points, then from Kinect depth image it gets the actual coordinates.

It works okay, but assums that the vision model is trained for the object. Actually the biggest limiting factor was the Baxter parallel gripper, super hard to grasp anything with it.

https://drive.google.com/open?id=1zDSLiC6MaF3uKHgFuAD15iJc5cERn5sP
