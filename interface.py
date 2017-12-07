#run this file to start program

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

from screenStart import *
from screenMoodSelect import *
from screenPlay import *
from openCVToTkinterFunctions import * #handle detection
from screenMoodDetect import *
import colors, random
from musicJud import *

####################################
# barebones from CMU 15112 website
####################################

def init(data):
    data.state = 0 #0 for start mode selection, 1 for mood sel, 2 for play music, 3 for mood det
    data.mood = -1 #0 happy, 1sad, 2 powerful, 3 peaceful
    data.answered = 0
    data.timer = 0

    #for storing current music info
    data.startLet = 'A'
    data.majorBool = 0
    data.chordProg = []
    data.melodyRhyth = []
    data.melodyPitches = []

    #below mostly for drawing as well as button coordinates
    dataScreenStart(data) #get data regarding startScreen (in startScreen)
    dataScreenMoodSel(data) #get data regarding mood selection screen (in screenMoodSelect)
    dataScreenPlay(data)
    dataScreenMoodDet(data)

def mousePressed(event, data):
    #backwards because mode switches cause the event to change
    if data.state == 3: #mood detection camera screen
        mouseScreenMoodDet(event, data)
    elif data.state == 2: #music screen
        mouseScreenPlay(event, data)
    elif data.state == 1: #mood selection screen
        mouseScreenMoodSel(event, data)
    elif data.state == 0: #start screen
        mouseScreenStart(event, data)

def keyPressed(event, data):
    pass

def timerFired(data):
    pass

def drawBackground(canvas, data): #random squares/triangles/ovals drawn as timer fired
    #pick color array
    if data.mood == -1:
        list = colors.greys
    elif data.mood == 0:
        list = colors.colsHap
    elif data.mood == 1:
        list = colors.colsSad
    elif data.mood == 2:
        list = colors.colsPow
    else:
        list = colors.colsPea
    for i in range (1, 20): #random shapes
        color = list[random.randint(0,3)]
        chooseShape = random.randint(0, 2)
        if chooseShape == 0:
            canvas.create_oval(random.randint(-data.width//5, data.width*6//5),
                                random.randint(-data.height//5, data.height*6//5),
                                random.randint(-data.width//5, data.width*6//5),
                                random.randint(-data.height//5, data.height*6//5),
                                fill = color, width = 0)
        elif chooseShape == 1:
            canvas.create_polygon(random.randint(-data.width//5, data.width*6//5), 
                              random.randint(-data.height//5, data.height*6//5), 
                              random.randint(-data.width//5, data.width*6//5), 
                              random.randint(-data.height//5, data.height*6//5), 
                              random.randint(-data.width//5, data.width*6//5), 
                              random.randint(-data.height//5, data.height*6//5), 
                              fill = color, width = 0)
        else: 
            canvas.create_rectangle(random.randint(-data.width//5, data.width*6//5),
                                random.randint(-data.height//5, data.height*6//5),
                                random.randint(-data.width//5, data.width*6//5),
                                random.randint(-data.height//5, data.height*6//5),
                                fill = color, width = 0)

def redrawAll(canvas, data):
    drawBackground(canvas, data)

    if data.state == 0: #start screen
        drawScreenStart(canvas, data)
    if data.state == 1: #mood selection screen
        drawScreenMoodSel(canvas, data)
    if data.state == 2: #play music screen
        drawScreenPlay(canvas, data)
    if data.state == 3: #mood detection screen
        drawCamera(canvas, data)
        drawCameraButtons(canvas, data)

####################################
# CHANGED RUN FUNCTION TO ACCOMMODATE CAMERA; ALL ADAPTED FROM
# BAREBONES, COURSE WEBSITE, AND OPEN CV DOCUMENTATION
####################################

def run(width=640, height=475):
    def redrawAllWrapper(canvas, data):
        if data.state == 3:
            #BELOW IF STATEMENT ADAPTED FROM CV DOCUMENTATION

            start = time.time()

            # Get the camera frame and get it processed.
            _, data.frame = data.camera.read()
            cameraFired(data)
            # Redrawing code
            canvas.delete(ALL)
            redrawAll(canvas, data)
            # Calculate delay accordingly
            end = time.time()
            diff_ms = (end - start) * 1000

            # Have at least a 5ms delay between redraw. Ideally higher is better.
            delay = int(max(data.redraw_delay - diff_ms, 5))

            root.after(delay, lambda: redrawAllWrapper(canvas, data))
        else:
            canvas.delete(ALL)
            canvas.create_rectangle(0, 0, data.width, data.height,
                                    fill=colors.lightGrey, width=0)
            redrawAll(canvas, data)
            canvas.update()

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        if data.state == 3:
            # Ensuring that the code runs at roughly the right periodicity
            start = time.time()
            timerFired(data)
            end = time.time()
            diff_ms = (end - start) * 1000
            delay = int(max(data.timer_delay - diff_ms, 0))
            root.after(delay, lambda: timerFiredWrapper(canvas, data))    # create the root and the canvas
        else:
            timerFired(data)
            redrawAllWrapper(canvas, data)
            # pause, then call timerFired again
            canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.camera_index = 0
    data.timerDelay = 100 # milliseconds
    data.timer_delay = 100 #milliseconds; for the camera
    data.redraw_delay = 50
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    try: #stop music if still playing
        pygame.mixer.music.fadeout(500)
    except:
        pass
    print("bye!")

run()
