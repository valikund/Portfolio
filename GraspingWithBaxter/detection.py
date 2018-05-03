import os
import sys
import random
import math
import numpy as np
import scipy.misc
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.decomposition import PCA as sklearnPCA

import coco
import utils
import model as modellib
import visualize


# Root directory of the project
ROOT_DIR = os.getcwd()

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Path to trained weights file
# Download this file and place in the root of your 
# project (See README file for details)
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")

class InferenceConfig(coco.CocoConfig):
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1

config = InferenceConfig()
# Create model object in inference mode.
model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

# COCO Class names
# Index of the class in the list is its ID. For example, to get ID of
# the teddy bear class, use: class_names.index('teddy bear')
class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']

# Load a random image from the images folder
#file_names = next(os.walk(IMAGE_DIR))[2]
#image = scipy.misc.imread(os.path.join(IMAGE_DIR, random.choice(file_names)))
#image = scipy.misc.imread("/home/valikund/darknet/data/dog.jpg")
image_path = sys.argv[1] 
image = scipy.misc.imread(image_path)

# Run detection
results = model.detect([image], verbose=0)

# Visualize results
r = results[0]
#visualize.display_instances(image, r['rois'], r['masks'], r['class_ids'], 
#                            class_names, r['scores'])
def findOutside(vec_x,vec_y):
    x,y = math.ceil(mid_x),math.ceil(mid_y)
    c= 0
    x_,y_ = [],[]
    while ((x>roi[0] and x<roi[2])  and (y>roi[1] and y<roi[3])):
        if(X[x,y] == 0):
            x_.append(x)
            y_.append(y)
            
        x = math.ceil(mid_x + c*vec_x)
        y = math.ceil(mid_y + c*vec_y)
        c += 1
    if(len(x_) == 0):
        return x,y
    else:
        return round(np.mean(x_)),round(np.mean(y_))

xx = []
yy = []
output = []
for i in range(len(r['rois'])):
    X = r['masks'][:,:,i]
    roi = r['rois'][i]
    X_new = []
    Y_new = []
    pca_in = []
    for k in range(X.shape[1]):
        for j in range(X.shape[0]):
            if X[j,k]:
                X_new.append(j)
                Y_new.append(k)
                pca_in.append([j,k])

    sklearn_pca = sklearnPCA()
    Y_sklearn = sklearn_pca.fit(pca_in).transform(pca_in)
    vec_x,vec_y = sklearn_pca.components_[1]
    mid_x,mid_y = np.mean(X_new),np.mean(Y_new)
    
    x_,y_ = findOutside(-vec_x,-vec_y)
    x2,y2 = findOutside(vec_x,vec_y)
    
    name = class_names[r['class_ids'][i]]
    xx.extend([y_,y2,mid_y])
    yy.extend([x_,x2,mid_x])
    output.append([i,name,round(mid_y),round(mid_x),y_,x_,y2,x2 ])
print(output)