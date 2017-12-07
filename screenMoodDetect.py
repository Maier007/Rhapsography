#screen for mood detection

import time
import sys
from tkinter import *
import tkinter as tk
import numpy as np
import cv2
from PIL import Image, ImageTk
import math
import collections
import coloredlogs
import logging
import colors

from pictureJud import *
from openCVToTkinterFunctions import *
import ctypes
import colors
from musicGen import *
from musicJud import *

#helper functions
def getButCoords(cX, cY, w, h): #returns SX, SY, EX, EY respectively
    butSX = cX - w
    butSY = cY - h
    butEX = cX + w
    butEY = cY + h
    return butSX, butSY, butEX, butEY

#data handling
def dataScreenMoodDet(data):
    data.camButtonX = data.width//2
    data.camButtonY = data.height*8//9
    data.camButtonRad = data.width//25
    pass

#event handling
def mouseScreenMoodDet(event, data):
    butSX, butSY, butEX, butEY = getButCoords(data.moodSelBackButnX, data.moodSelBackButnY, 
                                    data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    distX = event.x - data.camButtonX
    distY = event.y - data.camButtonY
    totalDist = distX**2 + distY**2
    #handle back button recycled from mood select
    if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
        data.state = 0
        data.camera = None
        playRandomNote()
        play_music('pitch.mid', 1)
    
    #handle camera button
    elif totalDist < data.camButtonRad**2:
        #take a picture
        newImage = data.frame
        cv2.imwrite("test.png", newImage)
        #reset and remeasure detect mood then change data.mood
        detectedMood = None
        detectedMood = detectMood(data, newImage)
        #change state and mood and generate music
        if detectedMood == None: #something went wrong
            errorText = """Make sure you are the only face near the camera.  This feature works best when your eyes are at eye level with the camera and you are about 12 inches away from the laptop.  """
            ctypes.windll.user32.MessageBoxW(0, errorText, "Error!", 1)
            data.state = 0
            data.camera = None
        else: #mood successfully detected
            data.mood = detectedMood
            data.state = 2
            data.answered = 0
            data.playing = 1
            data.camera = None
            data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches = generateNewMusic(data.mood)
            while judgeMusic(data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches) != data.mood:
                data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches = generateNewMusic(data.mood)
            play_music('output.mid', 100000)
    
    #clicked not on a button
    else:
        errorText = """Please click on a button!"""
        ctypes.windll.user32.MessageBoxW(0, errorText, "Error!", 1)
        data.state = 0
        data.camera = None
        

def drawCameraButtons(canvas, data):
    #draw back button
    SX, SY, EX, EY = getButCoords(data.moodSelBackButnX, data.moodSelBackButnY, 
                                    data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    canvas.create_rectangle(SX, SY, EX, EY, 
                            fill = colors.buttonStartBlack, width = 0)
    canvas.create_text(data.moodSelBackButnX, data.moodSelBackButnY, 
                    text = "back", fill = colors.greys[2], font = "system 20")
    
    #draw camera button
    SX, SY, EX, EY = getButCoords(data.camButtonX, data.camButtonY, data.camButtonRad, data.camButtonRad)
    canvas.create_oval(SX, SY, EX, EY, 
                        fill = "black", width = 0)