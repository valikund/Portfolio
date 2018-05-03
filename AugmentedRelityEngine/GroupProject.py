import pyyolo
import numpy as np
import cv2
from collections import deque
import numpy as np


class Filter(deque):
    # Filter out outbound values, which are probably errors
    # Make the speed bounded by using median filter
    def __init__(self, size=5):
        self.size = size
        self.que = deque(maxlen=size)
        self.treshold = 5 / size
    def append(self,point):
        #Initializing the filter
        self.que.append(point)
        return self.que
    def isAnomaly(self):
        if(len(self.que)) == 5:
            asdd = np.asarray(self.que)
            avg = asdd.mean(axis=0)
            avg = np.row_stack((avg, avg, avg,avg,avg))
            stdev = asdd.std(axis=0)
            stdev = np.row_stack((stdev, stdev, stdev,stdev,stdev))
            proximity = np.square(asdd) + np.square(avg) - 2 * np.multiply(asdd, avg)
            proximity = np.divide(proximity, 2 * self.size * np.square(stdev))
            proximity = np.sum(proximity, axis=1)
            if (asdd.shape[0] - 1 == np.argmax(proximity) and (np.max(proximity) - np.partition(proximity, -2)[-2]) > self.treshold):
                return 'anomaly'
            else :
                return ''

datacfg = '/home/valikund/darknet/data/papers.data'
cfgfile = '/home/valikund/darknet/cfg/papers.cfg'
weightfile = '/home/valikund/DarknetModels/old5k_new7k.weights'
thresh = 0.1
hier_thresh = 0.1

cam = cv2.VideoCapture(-1)
pyyolo.init(datacfg, cfgfile, weightfile)

filt = Filter(size=5)

while True:
    ret_val, img = cam.read()
    imgs = np.copy(img)
    img = img.transpose(2, 0, 1)
    c, h, w = img.shape[0], img.shape[1], img.shape[2]
    # print w, h, c
    data = img.ravel() / 255.0
    data = np.ascontiguousarray(data, dtype=np.float32)
    outputs = pyyolo.detect(w, h, c, data, thresh, hier_thresh)
    if outputs:
        output = outputs[0]
        x1, y1, x2, y2 = output['left'], output['top'], output['right'], output['bottom']
        filt.append([x1, y1, x2, y2])

        if filt.isAnomaly() == 'anomaly':
            cv2.rectangle(imgs, (x1, y1), (x2, y2), (0, 0, 255), 10)
        else:
            cv2.rectangle(imgs, (x1, y1), (x2, y2), (0, 150, 0), 10)
    cv2.imshow('frame', imgs)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite('output.jpg',imgs)
        break

# free model
pyyolo.cleanup()