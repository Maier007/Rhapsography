#all colors found in here

def rgbString(red, green, blue):
    return "#%02x%02x%02x" % (red, green, blue)

lightGrey = rgbString(216, 216, 216)
greys = [rgbString(230, 230, 230), rgbString(250, 250, 250), rgbString(190, 190, 190), \
        rgbString(160, 160, 160), rgbString(216, 216, 216)]
textGrey = rgbString(100, 100, 100)
playGrey = rgbString(50, 50, 50)
buttonStartBlue = rgbString(200, 200, 255)
buttonStartBlack = rgbString(0, 0, 0)

butnMoodHap = "#DBCF58"
butnMoodSad = "#664495"
butnMoodPow = "#D5565F"
butnMoodPea = "#58B549"
colsHap = ['#BBAE30', '#DBCF58', '#FFF48B', '#FFF8B1', '#FFFBD6']
colsSad = ['#4D297F', '#664495', '#8466AE', '#AD95CE', '#D5C7E9']
colsPow = ['#B72F39', '#D5565F', '#f98890', '#FBAEB4', '#FDD4D7']
colsPea = ['#389B28', '#58B549', '#81D473', '#A8E59F', '#D1F3CC']