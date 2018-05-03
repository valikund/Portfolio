import json

#Open the annoatation file
size = 600
path = '/home/valikund/Desktop/sloth/examples/example1_labels.json'
with open(path) as data_file:
    data = json.load(data_file)

positive = 1
negative = 1
f_train = open('/home/valikund/darknet/data/train.txt', 'w')
label_dir = "/home/valikund/darknet/data/labels/"

#Move pictures to training folder, and create image labels where the bounding box corrdinates can be found
for file in data:

    filename = str(file['filename'][9:])
    filename = "/home/valikund/" + filename

    for bounding_box in file['annotations']:

        w = bounding_box['width']
        h = bounding_box['height']
        x = bounding_box['x']
        if x < 0:
            x = 0
        x = (x + w/ 2) / size

        y = bounding_box['y']
        if y < 0:
            y = 0
        y = (y + h/ 2) / size

        w = w/size
        h = h/size
        line = "0 {0:.6f} {1:.6f} {2:.6f} {3:.6f} ".format(x,y,w,h)

        label_path = label_dir + filename[35:-4]+ '.txt'
        f = open(label_path, 'w')
        f.write(line)
        f.close()

        if (int(filename[35:-4]) < 251):
            f_train.write(filename[23:]+'\n')
            print(filename[23:])

f_train.close()
