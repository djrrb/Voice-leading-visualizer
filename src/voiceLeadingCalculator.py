# run in drawbot http://drawbot.com


# this object counts steps
class ToneCounter:
    tones = [1, 1.5, 2, 2.5, 3, 4, 4.5, 5, 5.5, 6, 6.5, 7]

    def __init__(self, tone=1):
        self.tone = tone
    
    def next(self):
        # bump to the next half step
        i = self.tones.index(self.tone)
        if i == len(self.tones)-1:
            self.tone = self.tones[0]
        else:
            self.tone = self.tones[i+1]
            
    def prev(self):
        # bump to the previous half step
        i = self.tones.index(self.tone)
        if i == 0:
            self.tone = self.tones[-1]
        else:
            self.tone = self.tones[i-1]


# my bank of chords
# right now using some non diatonic chords
chordBank = {
    1: [1, 3, 5],
    2: [2, 4.5, 6],
    3: [3, 5.5, 7],
    4: [4, 6, 1],
    5: [5, 7, 2],
    6: [6, 1, 3],
    7: [7, 2, 4],
    }


# a list of accepted semitones
tones = [1, 1.5, 2, 2.5, 3, 4, 4.5, 5, 5.5, 6, 6.5, 7]

# what is the range we want to see on our chart
tonalRange = tones[-5:] + tones + tones[:5]

fontName = 'InputMonoCompressed-Bold'
lightFontName = 'InputMonoCompressed-Regular'

# get inversions
def getInversion(chord, inversion):
    if inversion < 0:
        print(inversion)
    for inv in range(inversion):
        chord = chord[1:] + [chord[0]]
    return chord


pages = [


(
    'Blue Virginia Blues Verse (auto)',
    [
        (1, None),
        (3, None),
        (4, None),
        (1, None),
        (2, None),
        (5, None),
        (1, None),
        (3, None),
        (4, None),
        (1, None),
        (5, None),
        (1, None),
    ]
),
    
# (
#     'Blue Virginia Blues Verse (manual)',
#     [
#         (1, 0),
#         (3, 2),
#         (4, 2),
#         (1, 0),
#         (2, 0),
#         (5, 1),
#         (1, 0),
#         (3, 2),
#         (4, 2),
#         (1, 0),
#         (5, 1),
#         (1, 0),
#     ]
# ),
    
(
    'Blue Virginia Blues Chorus (auto)',
    [
        4, 
        5, 
        1, 
        4, 
        1, 
        5, 
        4, 
        5, 
        1, 
        4, 
        1, 
        4, 
        1
    ]
),


(
    'Blue Virginia Blues Chorus (manual)',
    [
        (4, 2),
        (5, 1), 
        (1, 0),
        
        (4, 2), 
        (1, 0), 
        (5, 1), 
        
        (4, 2), 
        (5, 1),
        (1, 0), 
        (4, 2),
        
        (1, 0), 
        (4, 2), 
        (1, 0)
    ]
),
    

]



# just for display purposes
chordNamesDict = {
    1: 'I',
    2: 'II',
    3: 'III',
    4: 'IV',
    5: 'V',
    6: 'VI',
    7: 'VII'
    }



def getDistance(chord1, chord2):
    """get the total distance between two chords"""
    total = 0
    for i in range(3):
        tone1 = chord1[i]
        tone2 = chord2[i]
        total += abs(getToneDistance(tone1, tone2))
    return total
    
def findMatchingTones(chord1, chord2):
    """which tone matches"""
    for toneIndex in range(3):
        tone1 = chord1[toneIndex]
        tone2 = chord2[toneIndex]
        if tone1 == tone2:
            return toneIndex

def getToneDistance(tone1, tone2, direction=None):    
    stepUp = 0
    stepDown = 0
    # if the tones match, return nothing
    if tone1 == tone2:
        return 0
    # count tones up
    t = ToneCounter(tone1)
    match = False
    while match is False:
        t.next()
        stepUp += 1
        if t.tone == tone2:
            match = True
    # count tones down
    t = ToneCounter(tone1)
    match = False
    while match is False:
        t.prev()
        stepDown -= 1
        if t.tone == tone2:
            match = True
    # if there is no direction, return the closest
    if direction is None:
        if abs(stepUp) < abs(stepDown):
            return stepUp
        else:
            return stepDown
    # or return the specific direction
    elif direction == 1:
        return stepUp
    elif direction == -1:
        return stepDown
                
            
            



def parseChordBlock(chordBlock):
    if type(chordBlock) is int:
        chordName = chordBlock
        inversionIndex = None 
    else:
        try:
            chordName, inversionIndex = chordBlock
        except:
            chordName = chordBlock[0]
            inversionIndex = None
    return chordName, inversionIndex


def displayWithSuffix(inversion):
    if inversion == 0:
        return 'Root'
    elif inversion == 1:
        return '1st'
    elif inversion == 2:
        return '2nd'
    else:
        return 'Root'


for pageNumber, (pageTitle, chordProgression) in enumerate(pages):
    
    
    print('Page:', pageTitle)
    

    
    prevChord = None
    chosenChords = []

    for i, chordBlock in enumerate(chordProgression):
        chordName, inversionIndex = parseChordBlock(chordBlock)

        
        chord = chordBank[chordName]


        if inversionIndex is not False and inversionIndex is not None and inversionIndex != 'auto':
            theChoice = getInversion(chord, inversionIndex)
        elif i == 0:
            totalDistance = 0 
            theChoice = chord
        else:
            print('\tauto choice')
            minDistance = 50000000
            theChoice = None

            for ii in range(3):
                inversion = getInversion(chord, ii)
                if findMatchingTones(prevChord, inversion) is not None:
                    print('\tmatching tone', findMatchingTones(prevChord, inversion))
                    theChoice = inversion
                    inversionIndex = ii
                    #print('match', inversion)
                    break
                
            if theChoice is None:
                for ii in range(3):
                    inversion = getInversion(chord, ii)
                    if getDistance(prevChord, inversion) < minDistance:
                        print('\t', inversion, 'distance', getDistance(prevChord, inversion))
                        theChoice = inversion
                        inversionIndex = ii
                    
                
        if prevChord:        
            totalDistance = getDistance(prevChord, theChoice)
        else:
            totalDistance = 0
                    
        print(theChoice)
        chosenChords.append((theChoice, inversionIndex, totalDistance))
        prevChord = theChoice




    newPage('LetterLandscape')
    
    

    margin = 80
    translate(margin, margin)

    mw = width()-margin*2
    mh = height()-margin*2

    col = mw/(len(chosenChords)-1)
    row = mh/len(tonalRange)
    
    font(fontName, 12)
    text(pageTitle, (-30, mh+30))
    font(lightFontName, 12)
    text(''+str(pageNumber+1), (mw, mh+30), align="right")
    font(lightFontName, 8)

    for thisRow, tone in enumerate(tonalRange):
        if '.' in str(tone):
            toneString = '#' + str(floor(tone))
        else:
            toneString = str(tone)
        text(toneString, (-25, thisRow*row-4), align="right")
        if '.' not in str(tone):
            with savedState():
                strokeWidth(.25)
                stroke(0)
                lineDash(1)
                line((0,  thisRow*row), (mw, thisRow*row))

    with savedState():
        for thisCol, chordBlock in enumerate(chordProgression):
            chordName, inversionIndex = parseChordBlock(chordBlock)
            font(fontName, 12)
            text(str(chordNamesDict[chordName]), (0, -40), align="center")
            font(lightFontName, 10)
            text(displayWithSuffix(chosenChords[thisCol][1]), (0, -60), align="center")
            translate(col)
        
    with savedState():
        for i, chordBlock in enumerate(chosenChords):
            if i > 0:
                chord, inversionIndex, totalDistance = chordBlock
                font(lightFontName, 10)
                text(str(totalDistance), (col/2, mh), align="center")
                translate(col)


    translate(0, tonalRange.index(1)*row)


    chordBases = []

    # loop through each of the three voices
    for toneIndex in range(3):
    
        with savedState():
            # set color
            if toneIndex == 0:
                theColor = 1, 0, 0
            elif toneIndex == 1:
                theColor = 1, 0, 1
            else:
                theColor = 0, 0, 1
            
            prevTone = None
            for chordIndex, chordBlock in enumerate(chosenChords):
                chord, inversionIndex, totalDistance = chordBlock
            
                tone = chord[toneIndex]
            
                if chordIndex == 0:
                    if toneIndex == 0:
                        pos = tones.index(tone)
                        chordBases.append((tone, pos))
                        pos*=row
                    else:
                        chordBaseTone, chordBasePos = chordBases[chordIndex]
                        pos = chordBasePos + getToneDistance(chordBaseTone, tone, direction=1)
                        pos*=row
                else:
                    if toneIndex == 0:
                        prevPos = pos
                        pos += getToneDistance(prevTone, tone)*row
                    else:
                        prevPos = pos
                        pos += getToneDistance(prevTone, tone, direction=None)*row
                with savedState():
                
                    translate(0, pos)
                
                    if prevTone:
                        with savedState():
                            strokeWidth(2)
                            stroke(*theColor)
                            blendMode('overlay')
                            line((0, 0), (-col, (prevPos-pos) ))
                            stroke(None)
                            fontSize(8)
                            text(
                                str(getToneDistance(prevTone, tone)), 
                                (-col/2, (prevPos-pos)/2+5), align="center")    
                    fill(*theColor)
                    oval(-20, -20, 40, 40)
                    fill(1)
                    font(fontName, 20)
                    text(str(tone).replace('.5', '#'), (0, -7), align="center")
                

                prevTone = tone
                translate(col)