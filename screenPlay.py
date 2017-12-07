#screen to play music

import colors
import math
from musicGen import *
from addToFile import *
from musicJud import *

#helper functions
def getButCoords(cX, cY, w, h): #returns SX, SY, EX, EY respectively
    butSX = cX - w
    butSY = cY - h
    butEX = cX + w
    butEY = cY + h
    return butSX, butSY, butEX, butEY

#data components
def dataScreenPlay(data):
    data.butPlayCX = data.width //2#* 7 // 18
    data.butPlayCY = data.height//2
    data.butPlayRBig = 100
    data.butPlayRSm = 80
    data.butnJudgeCX = (data.butPlayCX + data.butPlayRBig + data.width)//2
    data.butnJudgeW = data.width//5
    data.butnJudgeH = data.height//7
    data.butnJudgeCY = [data.height * 3//10, data.height * 31//70, data.height * 41//70, data.height * 51//70]

#event components
def mouseScreenPlay(event, data):
    #handle back button
    butSX, butSY, butEX, butEY = getButCoords(data.moodSelBackButnX, data.moodSelBackButnY, 
                                    data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
        data.state = 0
        data.mood = -1
        data.playing = 0
        pygame.mixer.music.fadeout(1500)
    
    #handle play/pause button as a square.. FIX
    distX = data.butPlayCX - event.x
    distY = data.butPlayCY - event.y
    if distX**2 + distY**2 < data.butPlayRSm**2:
        if data.playing == 0:
            pygame.mixer.music.play(1000)
            data.playing = 1
        else:
            pygame.mixer.music.fadeout(1500)
            data.playing = 0
    
    #handle judgeButtons
    for i in range(4):
        SX, SY, EX, EY = getButCoords(data.butnJudgeCX, data.butnJudgeCY[i], data.butnJudgeW//2, data.butnJudgeH//2)
        if event.x > SX and event.x < EX and event.y > SY and event.y < EY:
            data.answered = 1
   
            #format judged data
            
            judgeThis = []
            melodyContour = getMelodyContour(data.startLet, data.melodyPitches, data.majorBool)
            print(melodyContour)
            judgeThis.append(len(data.melodyPitches))
                #gets percentage count of jumps
            for k in range(7):
                count = 0
                for j in range(len(melodyContour)):
                    if abs(melodyContour[j]) == k:
                        count += 1
                judgeThis.append(count * 100 / len(data.melodyPitches))
            
            addData(data.majorBool, judgeThis, i)

def drawPlayButton(canvas, data):
    #backmost circle
    butSX, butSY, butEX, butEY = getButCoords(data.butPlayCX, data.butPlayCY, data.butPlayRBig, data.butPlayRBig)
    canvas.create_oval(butSX, butSY, butEX, butEY, fill = colors.buttonStartBlack, width = 0)
    #white circle
    butSX, butSY, butEX, butEY = getButCoords(data.butPlayCX, data.butPlayCY, data.butPlayRSm, data.butPlayRSm)
    canvas.create_oval(butSX, butSY, butEX, butEY, fill = colors.lightGrey, width = 0)
    #triangle
    triLeft = butSX + 30
    triRight = data.butPlayCX - 10
    triHeight = data.butPlayRSm - 20
    canvas.create_polygon(triLeft, data.butPlayCY - triHeight//2, triLeft, data.butPlayCY + triHeight//2, triRight, data.butPlayCY,
                            fill = "black", width = 0)
    #slash
    lineX = data.butPlayCX + (data.butPlayRSm - 20) * math.cos(math.pi/2)
    startY = data.butPlayCY - (data.butPlayRSm - 20) * math.sin(math.pi/2)
    endY = data.butPlayCY + (data.butPlayRSm - 20) * math.sin(math.pi/2)
    canvas.create_line(lineX, startY, lineX, endY, width = 5)
    
    #pause, approx same height as play button
    pauseC = (lineX + butEX) //2 -5
    pauseXLeft = pauseC - 10
    pauseXRight = pauseC + 10
    pauseTop = data.butPlayCY - triHeight//2
    pauseBot = data.butPlayCY + triHeight//2
    
    canvas.create_line(pauseXLeft, pauseTop, pauseXLeft, pauseBot, width = 10)
    canvas.create_line(pauseXRight, pauseTop, pauseXRight, pauseBot, width = 10)


def drawJudgeButtons(canvas, data): #to the right of the screen
    for i in range(4):
        SX, SY, EX, EY = getButCoords(data.butnJudgeCX, data.butnJudgeCY[i], data.butnJudgeW//2, data.butnJudgeH//2)
        color = data.moodButnColors[i]
        txt = data.moodButnText[i]
        # canvas.create_line(0, data.butnJudgeCY[i], data.width, data.butnJudgeCY[i])
        canvas.create_rectangle(SX, SY, EX, EY, fill = colors.buttonStartBlack, width = 0)
        canvas.create_text(data.butnJudgeCX, data.butnJudgeCY[i], text = txt, 
                            fill = color, font = "system 20")


#draw components and play music
def drawScreenPlay(canvas, data):
    #back button (recycled from mood-select-screen
    butnSX, butnSY, butnEX, butnEY = getButCoords(data.moodSelBackButnX, 
        data.moodSelBackButnY, data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    canvas.create_rectangle(butnSX, butnSY, butnEX, butnEY, 
                            fill = colors.buttonStartBlack, width = 0)
    canvas.create_text(data.moodSelBackButnX, data.moodSelBackButnY, 
                    text = "back", fill = colors.greys[2], font = "system 20")
    
    #yes/no button
    if data.answered == 0:
        drawJudgeButtons(canvas, data)
    #play/pause button
    drawPlayButton(canvas, data)
    
    #text
    moodList = ['happy', 'sad', 'powerful', 'peaceful']
    canvas.create_text(data.width//2, data.butPlayCY + data.butPlayRBig + 50, 
                    text = moodList[data.mood], fill = colors.textGrey, font = "system 20")
        
    