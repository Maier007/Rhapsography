#functions to place camera frames into tkinter

from tkinter import *
import time
import sys
import numpy as np
import cv2
from PIL import Image, ImageTk
import math
import collections
import coloredlogs
import logging

##below adapted mostly from opencv documentation to show video and detect and 
##show detections of smile/face/eyes
def opencvToTk(frame):
    """Convert an opencv image to a tkinter image, to display in canvas."""
    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # grey = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)
    # blurred = cv2.GaussianBlur(rgb_image, (5, 5), 0)
    # edges = cv2.Canny(rgb_image, 100, 50)
    # edges2 = cv2.Canny(rgb_image, 100, 50)
    # pil_img = Image.fromarray(edges + edges2)
    # tk_image = ImageTk.PhotoImage(image=pil_img)

    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')

    # img = cv2.imread('face1.jpg')
    gray = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2GRAY)

    #below, the format of code taken from 
    #https://github.com/VasuAgrawal/112-opencv-tutorial
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        rgb_image = cv2.rectangle(rgb_image,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = rgb_image[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),1)
        
        smile = smile_cascade.detectMultiScale(roi_gray,scaleFactor= 1.7,
            minNeighbors=22,minSize=(25, 25))

        # Set region of interest for smiles
        for (x, y, w, h) in smile:
            cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)

    # cv2.imshow('img',rgb_image)
    pil_img = Image.fromarray(rgb_image)
    tk_image = ImageTk.PhotoImage(image = pil_img)

    return tk_image

####CAMERA STUFF
def cameraFired(data):
    """Called whenever new camera frames are available."""
    # For example, you can blur the image.
    #data.frame = cv2.GaussianBlur(data.frame, (11, 11), 0)

def drawCamera(canvas, data):
    data.tk_image = opencvToTk(data.frame)
    canvas.create_image(data.width / 2, data.height / 2, image=data.tk_image)
