# python recognize.py --bounding-box "10,350,225,590"


# import the necessary packages
from gesturedetector import GestureDetector
from motiondetector import MotionDetector
from collections import deque
from vlcremote import VLCRemote
import sys
import numpy as np
import cv2
import json
# from pylab import arange

# construct the argument parser and parse the arguments


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    r = width / float(w)
    dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized



camera = cv2.VideoCapture(0)
cred = {}
vlc = VLCRemote()
command = ""

with open('credentials.txt', 'r') as f:
    cred = json.load(f)

try:
    vlc.login(cred['port'], cred['password'])
except Exception as e:
    raise e
    sys.exit(1)

# unpack the hand ROI, then initialize the motion detector and gesture detector
(top, right, bot, left) = np.int32("10,350,225,590".split(","))
gd = GestureDetector()
md = MotionDetector()

# initialize the total number of frames read thus far, a bookkeeping variable used to
# keep track of the number of consecutive frames a gesture has appeared in, along
# with the values recognized by the gesture detector
numFrames = 0
fingerDeque = deque(maxlen=10)
fingerDeque.appendleft(32)

# keep looping
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    numFrames+=1
    # resize the frame and flip it so the frame is no longer a mirror view
    frame = resize(frame, width=600)
    frame = cv2.flip(frame, 1)
    clone = frame.copy()
    (frameH, frameW) = frame.shape[:2]
    # extract the ROI, passing in right:left since the image is mirrored, then
    # blur it slightly
    roi = frame[top:bot, right:left]
    # shifted = cv2.pyrMeanShiftFiltering(roi, 21, 51)
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (9, 9), 0)
    thresh = None
    # if we have not reached 32 initial frames, then calibrate the skin detector
    if numFrames < 32:
        md.update(gray)

    # otherwise, detect skin in the ROI
    else:
        # detect motion (i.e., skin) in the image
        skin = md.detect(gray)

        # check to see if skin has been detected
        if skin is not None:
            # unpack the tuple and detect the gesture in the thresholded image
            (thresh, c) = skin
            cv2.drawContours(clone, [c + (right, top)], -1, (0, 255, 0), 2)
            fingers = gd.detect(thresh, c)
            fingerDeque.appendleft(fingers)

            if (np.mean(fingerDeque) == fingers):
                # GestureDetector.drawBox(clone, 0)
                GestureDetector.drawText(clone, 0, command)

                if (fingers == 0):
                    vlc.down()
                    command = "Volume Down"
                elif (fingers == 1):
                    vlc.up()
                    command = "Volume Up"
                elif (fingers == 2):
                    vlc.play()
                    command = "Play"
                elif ((fingers == 5) and (command is not "Pause")):
                    vlc.pause()
                    command = "Pause"
                print(fingers)

    # draw the hand ROI and increment the number of processed frames
    cv2.rectangle(clone, (left, top), (right, bot), (0, 0, 255), 2)
    numFrames += 1

    # show the frame to our screen
    # if thresh is not None:
    #     cv2.imshow("22", thresh)


    # maxIntensity = 255.0 # depends on dtype of image data
    # x = arange(maxIntensity)

    # # Parameters for manipulating image data
    # phi = 80
    # theta = 1

    # newImage1 = (maxIntensity/phi)*(clone/(maxIntensity/theta))**2

    # shifted = cv2.pyrMeanShiftFiltering(clone, 21, 51)
    cv2.imshow("Frame", clone)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# clean up the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
sys.exit(0)