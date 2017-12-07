#judges music

from musicGen import *
import musicData1 #data stored in here

#startLet, majMin, chordProgression, melodyRhyth, pitches = generateNewMusic()

## reformat
def convertPitchesToNumbers(startLet, melodyPitches, majMin):
    baseScale = generateScale(startLet, majMin)
    numberList = []
    for pitch in range(len(melodyPitches)):
        ind = baseScale.index(melodyPitches[pitch])
        numberList.append(ind)
    return numberList

def getMelodyContour(startLet, melodyPitch, majMin): #gets differences in pitches
    pitchInNumbers = convertPitchesToNumbers(startLet, melodyPitch, majMin)
    firstNumber = 0
    contour = []
    for i in range(0, len(pitchInNumbers)):
        contour.append(pitchInNumbers[i]-firstNumber)
        firstNumber = pitchInNumbers[i]
    return contour

## machine learning
def distance(l1, l2):
    #square of differences
    diffs = []
    for i in range(len(l1)):
        diffs.append((l2[i]-l1[i])**2)
    return sum(diffs)

## ADAPTED FROM Google tutorial on Youtube in Machine Learning
class myClassifier():  #finds closest point
    def fit(self, xTrain, yTrain):
        self.X = xTrain
        self.Y = yTrain
    def predict(self, test):
        currBestDiff = distance(test, self.X[0])
        bestIndex = 0
        for i in range(1, len(self.X)):
            compareThisDist = distance(test, self.X[i])
            if compareThisDist < currBestDiff:
                currBestDiff = compareThisDist
                bestIndex = i
        return self.Y[bestIndex]

def judgeMusic(startLet, majorBool, chordProg, melodyRhyth, melodyPitches): #returns a mood
    if majorBool == True:
        isMajor = 1
    else:
        isMajor = 0
    #match data based on major/minor (pitch jumps are different between major and minor)
    if isMajor == 1:
        xData = musicData1.XMajor
        yData = musicData1.YMajor
    else:
        xData = musicData1.XMinor
        yData = musicData1.YMinor
        
    #format judged data
    judgeThis = []
    melodyContour = getMelodyContour(startLet, melodyPitches, majorBool)
    # print(melodyContour)
    judgeThis.append(len(melodyPitches))
    #gets percentage count of jumps 0 - 6, in absolute value
    for i in range(7):
        count = 0
        for j in range(len(melodyContour)):
            if abs(melodyContour[j]) == i:
                count += 1
        judgeThis.append(count * 100 / len(melodyPitches))
    
    # print(judgeThis)
    my_classifier = myClassifier() #uses written classifier above (creates an instance to judge with)
    my_classifier.fit(xData, yData)
    prediction = my_classifier.predict(judgeThis)
    return prediction