import pyyolo
import numpy as np
from collections import deque
from StreamingRecognition import Client
from googletrans import Translator #using this because cloud translate does not work for me
from multiprocessing import Process, Pipe
import cv2
from math import fabs,ceil
from unidecode import unidecode
from scipy.signal import medfilt
import time
import re

class Filter(deque):
    # Filter out outbound values, which are probably errors
    # Make the speed bounded by using median filter
    def __init__(self, size=0):
        self.size = size
        self.speed = 50
        self.x = deque(maxlen=size)
        self.y = deque(maxlen=size)
    def append(self,x_new,y_new):
        #Initializing the filter
        self.x.append(x_new)
        self.y.append(y_new)
        return int(medfilt(self.x,self.size)[-1]), int(medfilt(self.y,self.size)[-1])

def drawText(mat,x1,y1,x2,y2,text,margin=50):
    #Encode text to ASCII
    text = unidecode(text)

    freeArea = int((x2-x1-margin*2)*(y2-y1-margin*2))
    fontsize = 8
    sizeArea = freeArea + 1
    rows = 1.0
    while (freeArea < sizeArea):
        size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, fontsize, fontsize)
        rows = int(ceil(float(size[0][0]) / (x2-x1-margin* 1.25)))
        sizeArea = int(size[0][0]*rows* (size[0][1] * 1.5 ))
        if freeArea < sizeArea:
            fontsize = int(fontsize/2)
            if not (fontsize > 0.4):
                rows = int(ceil(rows / 2))
                break

    font = cv2.FONT_HERSHEY_SIMPLEX

    for i in range(rows):
        cv2.putText(mat, text[:int(ceil(len(text)/(rows-i)))], (x1+2*margin,y1+margin + (i+1)*size[0][1]*2), font, fontsize, (0, 0, 0), fontsize*2)
        text = text[int(ceil(len(text)/(rows-i))):]
    return mat

def drawImage(mat,imageMat,x1,y1,x2,y2,margin=50):
    if (x2-x1-margin*2)>0 and (y2-y1-margin*2)>0:
        out_img = cv2.resize(imageMat,dsize=(x2-x1-margin*2,y2-y1-margin*2))
        mat[y1+margin:y2-margin,x1+margin:x2-margin,:] = out_img
    return mat

def translate_text(target, text):
    if text:
        translator = Translator()
        result = translator.translate(text, dest=target)
        print result.text
        return result.text
    else:
        return ''

def audio_source(conn,languageOut):
    voiceLanguage = 'en-US'
    textLanguage = 'en'
    while True:
        [voiceLanguage,textLanguage] = languageOut.recv()
        client = Client(language=voiceLanguage)
        speech = client.listen()
        #If the text language is not the same as the voice translate it
        if textLanguage not in voiceLanguage:
            translation = translate_text(textLanguage,speech)
            conn.send([speech, translation])
        else:
            conn.send([speech,speech])
    conn.close()
    languageOut.close()

def drawProcess(imgPipe ,textPipe ,inPipe,coordPipeOut ,outPipe):
    # imgPipe: input end of a pipe containing the path to image
    # textPipe: input end of a pipe containing the text to be printed
    # inPipe: input end of a pipe containing the webcam image
    # outPipe: output end of a pipe where we put the finished image
    timeStamp = 0
    currentText = None
    currentImage = None
    timout = 2.5  # in seconds
    f = open('log.txt', 'w')
    while True:
        if inPipe.poll():
            webcam = inPipe.recv()
            #cv2.imwrite('input.jpg',webcam)
            coord = coordPipeOut.recv()
            x1, y1 ,x2 ,y2 = coord[0] ,coord[1] ,coord[2] ,coord[3]
            #f.write("asd {} {} {} {}".format(x1,y1,x2,y2))
            # Checking wether the buffer is too old?

            if ((time.time() - timeStamp) > timout*2): #or imgPipe.poll()
                currentText = None
                currentImage = None
            elif ((time.time() - timeStamp) > timout) and (textPipe.poll() or imgPipe.poll() ): #or imgPipe.poll()
                currentText = None
                currentImage = None

            # If there is nothing to draw as of now check the pipes
            if (currentText is None) and (currentImage is None):
                # Text have precedence over text

                if textPipe.poll():
                    currentText = textPipe.recv()
                    timeStamp = time.time()
                elif imgPipe.poll():
                    currentImage = cv2.imread(imgPipe.recv())
                    timeStamp = time.time()



            # If there is an image in the buffer print it
            if (currentImage is not None):
                webcam = drawImage(webcam, currentImage, x1, y1, x2, y2, margin=50)
            elif (currentText is not None):
                webcam = drawText(webcam, x1, y1, x2, y2, currentText, margin=20)

            cv2.imwrite('output.jpg', webcam)
            outPipe.send(webcam)

#Initializing detector
datacfg = '/home/valikund/darknet/data/papers.data'
cfgfile = '/home/valikund/darknet/cfg/papers.cfg'
weightfile = '/home/valikund/DarknetModels/new11k.weights'
thresh = 0.1
hier_thresh = 0.1
pyyolo.init(datacfg, cfgfile, weightfile)

#Initializing time series
list = []

#Initializing audio feed
parent_conn, child_conn = Pipe() #pipe for passing back the texts
languageIn, languageOut = Pipe() #pipe for passing the languages
p = Process(target=audio_source, args=(child_conn,languageOut,))
p.start()

#Initializing printer feed
imgPipeIn, imgPipeOut = Pipe()
textPipeIn, textPipeOut = Pipe()
camPipeIn, camPipeOut = Pipe()
coordPipeIn, coordPipeOut = Pipe()
printPipeIn, printPipeOut = Pipe()
h = Process(target=drawProcess, args=(imgPipeOut ,textPipeOut ,camPipeOut,coordPipeOut ,printPipeIn,))
h.start()

cap = cv2.VideoCapture(0)

#Initialize the filters SIZE MUST BE ODD
top_corner = Filter(size=5)
bot_corner = Filter(size=5)

#Write on image init
font = cv2.FONT_HERSHEY_SIMPLEX
text = 'Hello World!'
imagePath = ('/home/valikund/PycharmProjects/AugmentedReality/Application/pl_flag.png')
imgFlag = True
textFlag = True
bStart = False

#Setting up the translator
currentWrittenLanguage = 'en' #so it wont print the flag all the time
currentSpokenLanguage = 'en-US'
languageIn.send([currentSpokenLanguage,currentWrittenLanguage])

while(True):
    # Capture frame-by-frame
    ret, img = cap.read()
    imgs = np.copy(img)
    # ret_val, img = cam.read()
    img = img.transpose(2, 0, 1)
    c, h, w = img.shape[0], img.shape[1], img.shape[2]
    # print w, h, c
    data = img.ravel() / 255.0
    data = np.ascontiguousarray(data, dtype=np.float32)

    outputs = pyyolo.detect(w, h, c, data, thresh, hier_thresh)

    #Getting the input text from the translator
    if parent_conn.poll():
        [original, text1] = parent_conn.recv()
        if text1:
            text = text1
            print text
##################################################
##################################################
            #The whole logic of the video
            #languageIn.send([voiceLang],textLang)
            #if re.search('magyar',asd,re.IGNORECASE):
            if re.search("subtitle", original, re.IGNORECASE):
                imgPipeIn.send('/home/valikund/PycharmProjects/AugmentedReality/Application/british_flag.png')

                bStart = True
            if bStart:
                textPipeIn.send(text)
                if re.search("polish", original, re.IGNORECASE) and (currentWrittenLanguage is not 'pl'):
                    imgPipeIn.send('/home/valikund/PycharmProjects/AugmentedReality/Application/pl_flag.png')
                    currentSpokenLanguage,currentWrittenLanguage = "en-US",'pl'
                elif re.search("italian", original, re.IGNORECASE) and (currentWrittenLanguage is not 'it'):
                    imgPipeIn.send('/home/valikund/PycharmProjects/AugmentedReality/Application/it_flag.png')
                    currentSpokenLanguage,currentWrittenLanguage = "en-US",'it'
                elif re.search("hungarian", original, re.IGNORECASE) and (currentWrittenLanguage is not 'en'):
                    imgPipeIn.send('/home/valikund/PycharmProjects/AugmentedReality/Application/hu_flag.jpg')
                    currentSpokenLanguage,currentWrittenLanguage = "hu-HU",'en'
                elif re.search("angol", original, re.IGNORECASE) and (currentWrittenLanguage is not 'en'):
                    imgPipeIn.send('/home/valikund/PycharmProjects/AugmentedReality/Application/british_flag.png')
                    currentSpokenLanguage, currentWrittenLanguage = "en-US",'en'
        languageIn.send([currentSpokenLanguage, currentWrittenLanguage])
##################################################
##################################################


    #Putting in the stuff to print
    if imgFlag:
        imgPipeIn.send(imagePath)
        imgFlag = False
    elif textFlag:
        textPipeIn.send(text)
        textFlag = False

    #Draw rectangle around paper
    if outputs:
        output = outputs[0]
        x1,y1 = top_corner.append(output['left'],output['top'])
        x2,y2 = bot_corner.append(output['right'],output['bottom'])
        #Without filter use this :
        x1,y1,x2,y2 = output['left'],output['top'],output['right'],output['bottom']
        cv2.rectangle(imgs,(x1,y1),(x2,y2),(255,0,0),2)
        camPipeIn.send(imgs)
        coord = [x1,y1,x2,y2]
        coordPipeIn.send(coord)
        imgs = printPipeOut.recv()

    cv2.imshow('frame', imgs)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
pyyolo.cleanup()
cap.release()
cv2.destroyAllWindows()