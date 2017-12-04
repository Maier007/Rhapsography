import colors
import cv2

#helper functions
def getButCoords(cX, cY, w, h): #returns SX, SY, EX, EY respectively
    butSX = cX - w
    butSY = cY - h
    butEX = cX + w
    butEY = cY + h
    return butSX, butSY, butEX, butEY

#data components
def dataScreenStart(data):
    #mood selection button
    data.selButnX = data.width * 1//3
    data.selButnY = data.height * 2 // 3
    data.selButnWidth = data.width//4
    data.selButnHeight = data.height//7
    data.playing = 0
    
    data.detButnX = data.width * 2 // 3

#event-related components
def mouseScreenStart(event, data):
    #handle start button
    butSX, butSY, butEX, butEY = getButCoords(data.selButnX, data.selButnY, 
                                    data.selButnWidth//2, data.selButnHeight//2)
    if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
        data.state = 1
    butSX, butSY, butEX, butEY = getButCoords(data.detButnX, data.selButnY, 
                                    data.selButnWidth//2, data.selButnHeight//2)
    if event.x > butSX and event.x < butEX and event.y > butSY and event.y < butEY:
        data.state = 3
        #initialize camer
        camera = cv2.VideoCapture(data.camera_index)
        data.camera = camera
        data.timer = 0


#draw components
def drawScreenStart(canvas, data):
    #title
    canvas.create_text(data.width//2, data.height//3, text = "Rhapsography", 
                        fill = colors.textGrey, font = "Helvetica 50")
    
    #draw mood selection button
    butSX, butSY, butEX, butEY = getButCoords(data.selButnX, data.selButnY, 
                                    data.selButnWidth//2, data.selButnHeight//2)
    canvas.create_rectangle(butSX, butSY, butEX, butEY, 
                            fill = colors.buttonStartBlack, width = 1)
    canvas.create_text(data.selButnX, data.selButnY, text = "SELECT", 
                        fill = colors.lightGrey, font = "Helvetica 23")
    
    #draw mood detection button
    butSX, butSY, butEX, butEY = getButCoords(data.detButnX, data.selButnY, 
                                    data.selButnWidth//2, data.selButnHeight//2)
    canvas.create_rectangle(butSX, butSY, butEX, butEY, 
                            fill = colors.buttonStartBlack, width = 1)
    canvas.create_text(data.detButnX, data.selButnY, text = "DETECT", 
                        fill = colors.lightGrey, font = "Helvetica 23")
    