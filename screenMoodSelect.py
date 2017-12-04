import colors
from musicGen import *
from musicJud import *

##helper function
def getButCoords(cX, cY, w, h): #returns SX, SY, EX, EY respectively
    butSX = cX - w
    butSY = cY - h
    butEX = cX + w
    butEY = cY + h
    return butSX, butSY, butEX, butEY

##data components
def dataScreenMoodSel(data):
    #mood selection buttons, [happy, sad, powerful, peaceful]
    data.moodButnX = [data.width//4, data.width*3//4, data.width//4, data.width*3//4]
    data.moodButnY = [data.height-160, data.height-160, data.height-85, data.height-85]
    data.moodButnW = data.width*2//5
    data.moodButnH = data.height//7
    data.moodButnColors = [colors.butnMoodHap, colors.butnMoodSad, 
                            colors.butnMoodPow, colors.butnMoodPea]
    data.moodButnText = ["HAPPY", "SAD", "POWERFUL", "PEACEFUL"]
    
    #back button
    data.moodSelBackButnX = data.width//11
    data.moodSelBackButnY = data.height//12
    data.moodSelBackButnW = data.width//7
    data.moodSelBackButnH = data.height/11

##event-related components
def mouseScreenMoodSel(event, data):
    #handle back button
    butSX, butSY, butEX, butEY = getButCoords(data.moodSelBackButnX, data.moodSelBackButnY, 
                                    data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
        data.state = 0
    
    #handle four mood buttons
    for i in range(4):
        butSX, butSY, butEX, butEY = getButCoords(data.moodButnX[i], 
                        data.moodButnY[i], data.moodButnW//2, data.moodButnH//2)
        if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
            data.state = 2
            data.answered = 0
            data.mood = i
            print(data.moodButnText[data.mood])
            data.playing = 1
            break
    if data.state == 2:
        
        data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches = generateNewMusic(data.mood)
        while judgeMusic(data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches) != data.mood:
            data.startLet, data.majorBool, data.chordProg, data.melodyRhyth, data.melodyPitches = generateNewMusic(data.mood)
        play_music('output.mid')
        data.playing = 1

##draw components
def drawScreenMoodSel(canvas, data):
    #instructions
    canvas.create_text(data.width//2, data.height//3, text = "Select your mood", 
                    fill = colors.textGrey, font = "Helvetica 40")
    
    #back button
    butnSX, butnSY, butnEX, butnEY = getButCoords(data.moodSelBackButnX, 
    data.moodSelBackButnY, data.moodSelBackButnW//2, data.moodSelBackButnH//2)
    canvas.create_rectangle(butnSX, butnSY, butnEX, butnEY, 
                            fill = colors.lightGrey, width = 0)
    canvas.create_text(data.moodSelBackButnX, data.moodSelBackButnY, 
                    text = "BACK", fill = colors.textGrey, font = "Helvetica 15")
    
    for i in range(4): #four mood buttons
        butSX, butSY, butEX, butEY = getButCoords(data.moodButnX[i], 
                            data.moodButnY[i], data.moodButnW//2, data.moodButnH//2)
        color = data.moodButnColors[i]
        txt = data.moodButnText[i]
        canvas.create_rectangle(butSX, butSY, butEX, butEY, fill = colors.buttonStartBlack)
        canvas.create_text(data.moodButnX[i], data.moodButnY[i], text = txt, 
                            fill = color, font = "Helvetica 20")