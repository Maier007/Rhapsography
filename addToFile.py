def readFile(path):
    with open(path, "rt") as f:
        return f.read()

def writeFile(path, contents):
    with open(path, "wt") as f:
        f.write(contents)

def addToFile(path, contents):
    fullText = readFile(path)
    fullText += contents
    writeFile(path, fullText)

def addData(isMajor, newX, newY): #create new text and places into original file
    fullText = readFile('musicData1.py')
    newText = []
    if isMajor: #split upon cases if it is major or minor
        for line in fullText.splitlines():
            if line.startswith("XMaj"):
                newText.append("XMajor = [" + str(newX) + "," + line[10:])
            elif line.startswith("YMaj"):
                newText.append("YMajor = [" + str(newY) + ", " + line[10:])
            else:
                newText.append(line)
    else:
        for line in fullText.splitlines():
            if line.startswith("XMin"):
                newText.append("XMinor = [" + str(newX) + "," + line[10:])
            elif line.startswith("YMin"):
                newText.append("YMinor = [" + str(newY) + ", " + line[10:])
            else:
                newText.append(line)
    finalString =  ""
    for line in newText:
        finalString += line + "\n"
    writeFile('musicData1.py', finalString)