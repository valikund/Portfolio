# Development of an Augmented Reality Engine Based on Real-time Object Detection

The project is based on the DarkNet framework. I have collected a dataset and trained a YOLO2 classifier. The application relies on heavy parallel computations and asyncronous threads. Also implemented an anomaly detection algorithm from a recent paper for more reliability.

The most interesting parts of the work:
- Collecting a dataset from internet
- Handlabelling and cleaning the dataset
- Training the set on Goolge CLoud VMs
- Using threads and asyncronous pipes for realtime performance
- Experimented with different filters and anomaly detection algorithms for better performance
- Using voice and translation apis
- Live webcam feed
- Wrote everything as a paper

The files:
- RedditImageGrab.py : donwloads the images from reddit
- ImageProcessingDarknet.py : preprocesses the images, resizes the image and the bounding box
- StreamingRecognition.py : class for Google Speech realtime speech-to-text Api
- StreamTest.py : the main function, run this for results
- GroupProject.py : here instead of median filter I used anomaly detection to see whether it gives better performance (it does)
- development-augmented-reality .pdf : the papar, wrote it, did not try to publish it

Video: https://www.youtube.com/watch?v=RY7PWVt2vWE
