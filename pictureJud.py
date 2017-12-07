#judges a picture that is taken and stored

import numpy as np
import cv2
import random

def detectHappyOrPeace():
    pass

def detectMood(data, imageInfo): 
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
    smile_cascade = cv2.CascadeClassifier('haarcascade_smile.xml')
    
    #picture stored in test.png
    img = cv2.imread('test.png')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) != 1:  #make sure only one face detected
        # print("toomanyfaces")
        return None
        
    x = faces[0][0]
    y = faces[0][1]
    w = faces[0][2]
    h = faces[0][3]
    #limits search for smile/eyes to face
    img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    
    #uses gray face to find smile
    smile = smile_cascade.detectMultiScale(roi_gray, scaleFactor= 1.7,
        minNeighbors=22, minSize=(25, 25))
    if len(smile) > 0:
        sx = smile[0][0]
        sy = smile[0][1]
        sw = smile[0][2]
        sh = smile[0][3]
        smileImageColor = roi_color[sy:sy+sh, sx:sx+sw]
        # cv2.imshow('img',smileImageColor)
        
        #boundary of teeth color
        lower = np.array([150, 150, 150], dtype = "uint8")
        upper = np.array([255, 255, 255], dtype = "uint8")
        
        mask = cv2.inRange(smileImageColor, lower, upper)
        
        # cv2.imshow('mask',mask)
        # cv2.imshow('image', smileImageColor)
        output = cv2.bitwise_and(smileImageColor, smileImageColor, mask = mask)
        # cv2.imshow("images", np.hstack([smileImageColor, output]))
        
        #if there is white, it is a chance of happiness or peacefulness.  
        if np.any(mask):
            # print("teeth might be detected")
            guess = random.randint(0, 10)
            if guess < 8:
                return 0
                # print("happiness guessed")
            else:
                return 3
                # print("peace guessed")
        else:
            # print("teeth not detected")
            guess = random.randint(0, 10)
            if guess < 8:
                return 3
            else:
                return 0
        
    #uses gray face to find eyes
    eyes = eye_cascade.detectMultiScale(roi_gray)
    sumEyeDist = 0
    for (ex,ey,ew,eh) in eyes:
        #find the two main eyes based on similarity of size and y level
        #find height of eyes as related to the picture
        cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        sumEyeDist += ey
    avgEyeDist = ey/2
    totalEyeDistFromTop = avgEyeDist + y + eh//2
    if totalEyeDistFromTop > data.height//2:
        # print("Sadness detected")
        return 1
    else:
        # print("Powerfulness detected")
        return 2