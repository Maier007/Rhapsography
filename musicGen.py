from EasyMIDI import EasyMIDI,Track,Note,Chord,RomanChord
import pygame
import random
import copy

##reformats information
def getChordProgression(chords):
    bigChords = []
    for i in range(len(chords)):
        bigChords.append(chords[i][0])
    return bigChords

## music generation
#reorients scale into major/harmonic minor based on letter and major/minor bool
def generateScale(startLet, majorBool): 
    generalScale = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    indStartLetter = generalScale.index(startLet)
    
    #reorients scale to have first letter be the chosen letter
    generalScale = generalScale[indStartLetter:] + generalScale[:indStartLetter]
    
    notes = []
    if majorBool == 1:  #if major
        for i in [0, 2, 4, 5, 7, 9, 11]:
            notes.append(generalScale[i])
    else: #if minor
        for i in [0, 2, 3, 5, 7, 8, 11]:
            notes.append(generalScale[i])
    return notes

#creats base rhythm
def generateBaseBeat():
    #so we're going to assume that there's 4 measures in the entire melody
    #the difference is that there can be either 3 or 4 quarternotes in a measure
    #more would be distracting
    topSignatureNumber = random.randint(3, 4)
    
    chordBeat = []
    for i in range (4):
        chordBeat.append([])
        for j in range(topSignatureNumber):
            chordBeat[i].append('')
    
    return chordBeat

#chords always filled in on first beat, and randomly filled in for others
def generateChords(beat):
    #this will be based upon roman numeral notation
    romanNumerals = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
    filledBeat = copy.deepcopy(beat)
    filledBeat[0][0] = 'I'
    for i in range(1, 4): #for each of 4 measures
        chord = random.randint(1, 6)
        filledBeat[i][0] = romanNumerals[chord]
    for i in range(0, 4): #for each of the 4 measures
        for beat in range(1, len(filledBeat[0])):  #for each of the three/four beats
            filled = random.randint(0, 3)
            if filled == 3:
                filledBeat[i][beat] = filledBeat[i][0]
            else:
                filledBeat[i][beat] = 'R'
    
    return filledBeat

#so chords are held until next chord
def generateChordDurations(filledChords):
    chordLen = 1/len(filledChords[0])
    newChordList = []
    chordDurationList = []
    for i in range(len(filledChords)):
        for j in range(len(filledChords[i])):
            if filledChords[i][j] == 'R':
                pass
            else:
                count = 1
                index = j+1
                while index < len(filledChords[0]) and filledChords[i][index] == 'R':
                    count += 1
                    index += 1
                newChordList.append(filledChords[i][j])
                chordDurationList.append(chordLen * count)
    return newChordList, chordDurationList

def generateMelodyRhythm(beatPerMeas): #generates durations of melody notes
    #fixed so no infinite loop with weird durations
    possibleDurations = [1/4, 1/2, 1, 2, 3, 4, 5]
    durationList = []
    
    #fill the duration list until it is the right length
    while sum(durationList) != beatPerMeas * 4:
        newBeat = random.randint(0, 6)
        if sum(durationList) + possibleDurations[newBeat] <= beatPerMeas*4:
            durationList.append(possibleDurations[newBeat])
    
    #shuffle so longer notes can be at end too (less of chance to be at end otherwise)
    random.shuffle(durationList)
    return durationList

#generates pitches based on scale and duration list
def generateMelodyPitch(scale, durationList): 
    pitchList = []
    #fill in pitch for each spot in durationList
    for i in range(len(durationList)):
        pitchList.append(scale[random.randint(0, 6)])
    return pitchList

#generates everything, creates a file, and returns parameters to be judged
def generateNewMusic(MOOD):
    newSong = EasyMIDI()
    melody = Track("acoustic grand piano")
    chords = Track("acoustic grand piano")
    
    #creates the key
    notes = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    majMin = random.randint(0, 1) #0 for minor, 1 for major
    baseNote = random.randint(0, 6) #ABCDEFG
    baseScale = generateScale(notes[baseNote], majMin)
    
    #generate chord beat
    baseBeat = generateBaseBeat()
    #generate melody beat
    melodyRhyth = generateMelodyRhythm(len(baseBeat[0]))
    #generate chords
    getChords = generateChords(baseBeat)
    #generate melody
    pitches = generateMelodyPitch(baseScale, melodyRhyth)
    
    #add notes to melody
    for i in range(len(pitches)):
        if MOOD == 0:
            vol = random.randint(50, 100)
        elif MOOD == 1:
            vol = random.randint(50, 90)
        elif MOOD == 2:
            vol = random.randint(90, 100)
        else:
            vol = random.randint(50, 80)
        newNote = Note(pitches[i], octave = 5, duration = melodyRhyth[i]/4, volume = vol)
        melody.addNotes([newNote])
    
    #formats into boolean for chords
    if majMin == 0:
        majMin = False
    else:
        majMin = True
    
    #flattens chord list and gets durations
    newGetChords, chordDurations = generateChordDurations(getChords)
    
    chordOctave = random.randint(2, 4)
    
    #hardcoded chord volumes based on if powerful
    if MOOD == 2 or MOOD == 0:
        vol = random.randint(80, 100)
    else:
        vol = random.randint(40, 90)
    for i in range(len(newGetChords)):
        chords.addNotes(RomanChord(newGetChords[i], octave = chordOctave, duration = chordDurations[i], 
                        key = notes[baseNote], major = majMin, volume = vol))

    #place tracks into file
    newSong.addTrack(melody)
    newSong.addTrack(chords)
    newSong.writeMIDI('output.mid')
    
    #for debugging purposes
    # print(getChords)
    # print(melodyRhyth)
    # print(pitches)
    # print("MajorBool:  " + str(majMin))
    # print(newGetChords)
    # print(chordDurations)
    
    chordProgression = getChordProgression(getChords)
    
    #returns raw data so it is judged
    print( notes[baseNote], majMin, chordProgression, melodyRhyth, pitches)
    return notes[baseNote], majMin, chordProgression, melodyRhyth, pitches

 ## ADAPTED FROM https://www.daniweb.com/programming/software-development/code/216976/play-a-midi-music-file-using-pygame
def play_music(music_file):
    clock = pygame.time.Clock()
    freq = 44100    # audio CD quality
    bitsize = -16   # unsigned 16 bit
    channels = 2    # 1 is mono, 2 is stereo
    buffer = 1024    # number of samples
    pygame.mixer.init(freq, bitsize, channels, buffer)
    try:
        pygame.mixer.music.load(music_file)
        print ("Music file %s loaded!" % music_file)
    except pygame.error:
        print ("File %s not found! (%s)" % (music_file, pygame.get_error()))
        return
    playing = True
    pygame.mixer.music.play(10000)