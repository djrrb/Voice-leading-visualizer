##############################
# Draw a voice leading chart #
##############################

# Preferences

# the relative path to the markup file
plaintextPath = 'voiceLeading/WhereTheWildRiverRolls.voiceLeading'

# how many tones to show above and below the root
semitonesAbove = 12
semitonesBelow = 6

# connect lines for possible paths below this threshhold
possiblePathMaxDistance = 6

flatSharpMode = 1 # 0 is sharps, 1 is flats

# invert the entire chart
globalInversion = 0

# show in a particular key (beta)
showInKey = False
key = 'C'

#############
# Constants #
#############

semitones = {
    0: '1',
    1: ['#1', 'b2'],
    2: '2',
    3: ['#2', 'b3'],
    4: '3',
    5: '4',
    6: ['#4', 'b5'],
    7: '5',
    8: ['#5', 'b6'],
    9: '6',
    10: ['#6', 'b7'],
    11: '7',
    }
    
# calculate a map of semitones to the notes in the key
if flatSharpMode:
    notes = ['A', 'Bb', 'B', 'C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab']
else:
    notes = ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']

notesInKey = notes[notes.index(key):] + notes[:notes.index(key)]
semitonesInKey = dict(zip(range(12), notesInKey))

voiceColors = {
    0: (1, 0, 0),
    1: (1, 0, 1),    
    2: (0, 0, 1),    
    }
    
# all of the known chords
chordBank = {
    # diatonic
    'I': ['1', '3', '5'],
    'ii': ['2', '4', '6'],
    'iii': ['3', '5', '7'],
    'IV': ['4', '6', '1'],
    'V': ['5', '7', '2'],
    'vi': ['6', '1', '3'],
    'vii': ['7', '2', '4'],
    # other
    'II': ['2', '#4', '6'],
    'III': ['3', '#5', '7'],
    'bIII': ['b3', '5', 'b7'],
    'bVII': ['b7', '2', '4'],
    'Vsus4': ['5', '1', '2'],
    }

fontName = 'InputMonoCompressed-Bold'
lightFontName = 'InputMonoCompressed-Regular'
theFontSize = 9
theMedFontSize = 12
theBigFontSize = 18

####################
# Helper functions #
####################

def normalizeSemitone(semitone):
    return semitone % 12

def semitoneToTone(semitone, mode=0):
    tone = semitones[normalizeSemitone(semitone)]
    if type(tone) is list:
        return tone[mode]
    else:
        return tone
        
def toneToSemitone(semitone, octaveOffset=0):
    toneToSemitoneMap = {}
    for k, v in semitones.items():
        if type(v) is not list:
            v = [v]
        for i in v:
            toneToSemitoneMap[i] = k
    return toneToSemitoneMap[semitone] + octaveOffset*12
    
def parsePlaintext(myText):
    lines = myText.split('\n')
    pages = []
    currentTitle = None
    currentPage = []
    currentChords = []
    for line in lines:
        if not line:
            continue
        elif line[0] == '#':
            currentTitle = line[1:].strip()
        elif line[0] == '-':
            currentPage = [currentTitle, currentChords]
            pages.append(currentPage)
            currentTitle = None
            currentChords = []
            currentPage = []
        else:
            segments = line.split('|')
            cleanedSegments = []
            for si, segment in enumerate(segments):
                segment = segment.strip()
                try:
                    segment = int(segment)
                except:
                    pass
                if not segment:
                    segment = None
                cleanedSegments.append(segment)
            currentChords.append(tuple(cleanedSegments))
    if currentChords:
        currentPage = [currentTitle, currentChords]
        pages.append(currentPage)
    return pages
   

########
# Prep #
########
  
#process file
with open(plaintextPath, 'r', encoding='utf-8') as myFile:
    myText = myFile.read()
    pages = parsePlaintext(myText)

# determine height of chart
tonalRange = list(range(-semitonesBelow, semitonesAbove))

# create each page one at a time
pageNumber = 0

########
# Run! #
########

# loop through pages
for pageTitle, chordProgression in pages:
    
    newPage('LetterLandscape')
    
    # if the first entry does not have a chord
    # it is lead-in lyrics and can be printed in the margin
    leadInLyrics = None
    if chordProgression[0][0] == None:
        leadInLyrics = chordProgression[0][2]
        chordProgression = chordProgression[1:]

    # determine page margins
    margin = 80
    translate(margin, margin)

    mw = width()-margin*2
    mh = height()-margin*2

    colWidth = mw/(len(chordProgression)-1)
    rowHeight = mh/len(tonalRange)
    
    # set the title
    font(lightFontName, theFontSize)
    text(pageTitle, (-30, mh+40))
    # page number
    font(lightFontName, theFontSize)
    text(str(pageNumber+1), (mw, mh+30), align="right")
    font(lightFontName, theFontSize)
    
    # move to height of 1 chord
    # higher notes are positive, lower notes are negative
    translate(0, semitonesBelow*rowHeight)

    # print row labels
    for thisRow in tonalRange:
        toneString = semitoneToTone(thisRow, mode=flatSharpMode)
        text(toneString, (-25, thisRow*rowHeight-4), align="right")
        with savedState():
            # if the tone is a sharp or a flat, set a different line dash
            try:
                int(toneString)
                lineDash(1)
            except:
                lineDash(1, 2)           
            strokeWidth(.25)
            stroke(0)
            line((0,  thisRow*rowHeight), (mw, thisRow*rowHeight))
        
    # draw network of possible paths
    with savedState():
        # record previous semitones to draw a line
        prevSemitones = []
        for chordBlock in chordProgression:
            # the chord block may or may not have lyrics associated
            try:
                chordName, inversionIndex = chordBlock
            except:
                chordName, inversionIndex, lyrics = chordBlock

            if chordName is not None:

                tones = chordBank[chordName]
                
                # vertical line
                with savedState():
                    strokeWidth(.25)
                    stroke(0)
                    lineDash(1)
                    line((0, -semitonesBelow*rowHeight), (0, (semitonesAbove-1)*rowHeight))
        
                # calculate possible semitones shown in chart
                chordSemitones = []
                for thisRow in tonalRange:
                    toneString = semitoneToTone(thisRow, flatSharpMode)
                    if toneString in tones:
                        fill(.75)
                        oval(-8, thisRow*rowHeight-8, 16, 16)
                        chordSemitones.append(thisRow)
                
                        # draw lines to possible semitones if they are close enough
                        for prevSemitone in prevSemitones:
                            if abs(thisRow-prevSemitone) <= possiblePathMaxDistance:
                                with savedState():
                                    stroke(.75)
                                    line((0, thisRow*rowHeight), (-colWidth, prevSemitone*rowHeight))
                # set current semitones to previous
                prevSemitones = chordSemitones
            # move to the right
            translate(colWidth)
    
    # convert tones to semitones
    chordProgressionInSemitones = []
    for chordBlock in chordProgression: 
        try:
            chordName, inversionIndex = chordBlock
            lyrics = None
        except:
            chordName, inversionIndex, lyrics = chordBlock
        
        # if we were gonna auto-calculate, it would be here
        if inversionIndex is None:
            inversionIndex = 0

        if chordName is not None:

            tones = chordBank[chordName]
                
            inversionIndex += globalInversion

            chordSemitones = []
            firstSemitone = toneToSemitone(tones[0])
            for tone in tones:
                st = toneToSemitone(tone)
                if st < firstSemitone:
                    st += 12
                chordSemitones.append(st)
            
            if inversionIndex > 0:
                for ii in range(inversionIndex):
                    chordSemitones = chordSemitones[1:] + [chordSemitones[0]+12]
            if inversionIndex < 0:
                for ii in range(abs(inversionIndex)):
                    chordSemitones = [chordSemitones[-1]-12] + chordSemitones[:2]
            
            chordProgressionInSemitones.append(chordSemitones)
        else:
            chordProgressionInSemitones.append(None)

    # make an empty list to keep track of the total distance of chord movements
    chordDiffTotals = []
    for i in range(len(chordProgressionInSemitones)):
        chordDiffTotals.append(0)
    
    # loop through each voice and draw the path
    for voiceIndex in range(3):
        # keep track of the previous semitone
        prevSt = None
        with savedState():
            for chordIndex, chordSemitones in enumerate(chordProgressionInSemitones):
                if chordSemitones is not None:
                    st = chordSemitones[voiceIndex]
                    tone = semitoneToTone(st, flatSharpMode)
                    fill(*voiceColors[voiceIndex])
                    
                    if prevSt is not None:
                        # draw the line
                        with savedState():
                            stroke(*voiceColors[voiceIndex])
                            strokeWidth(3)   
                            blendMode('color')
                            diff = abs(st - prevSt)
                            line((0, st*rowHeight), (-colWidth, prevSt*rowHeight))
                        # draw the semitone distance
                        with savedState():
                            font(lightFontName, theFontSize)
                            text(str(diff), (-colWidth/2, (st + prevSt)*(rowHeight)/2 + 8   ), align='center')
                        chordDiffTotals[chordIndex] += diff
                    
                    # draw the oval

                    oval(-18, -18+st*rowHeight, 36, 36)
                    fill(1)
                    font(fontName, theBigFontSize)
                    # draw the tone text
                    toneText = tone
                    if showInKey:
                        toneText = semitonesInKey[st % 12]
                    text(toneText, (0, st*rowHeight-6), align="center")
            
                    # set current to previous
                    prevSt = st
                # move to the right
                translate(colWidth)
    
    # draw chord diff totals
    with savedState():
        translate(-colWidth/2)
        for chordDiffIndex, chordDiffTotal in enumerate(chordDiffTotals):
            if chordDiffIndex != 0:
                text(str(chordDiffTotal), (0, -semitonesBelow*rowHeight-37), align="center")
            translate(colWidth)
        
    # draw lead-in lyrics
    if leadInLyrics:
        with savedState():
            font(fontName, theFontSize)
            lineHeight(theFontSize*1.2)
            textBox(leadInLyrics, (-50, (semitonesAbove-1)*rowHeight, 30, 36), align="right")

    # draw chord names, inversions, and lyrics
    with savedState():
        for chordBlock in chordProgression: 
            try:
                chordName, inversionIndex = chordBlock
                lyrics = None
            except:
                chordName, inversionIndex, lyrics = chordBlock
                
            # draw chord name
            if chordName:
                font(fontName, theMedFontSize)
                text(chordName, (0, semitonesBelow*-rowHeight-35), align="center")
            
            # draw inversion text (normalized)
            if inversionIndex:
                remainder = inversionIndex % 3
                if remainder == 0:
                    inversionLabel = 'Root'
                elif remainder == 1:
                    inversionLabel = '1st'
                elif remainder == 2:
                    inversionLabel = '2nd'
                font(lightFontName, theFontSize)
                text(inversionLabel, (0, semitonesBelow*-rowHeight-50), align="center")
            
            # draw lyrics
            if lyrics:
                with savedState():
                    font(fontName, theFontSize)
                    lineHeight(theFontSize*1.2)
                    textBox(lyrics, (0, (semitonesAbove-1)*rowHeight, colWidth-2, 36), align="left")
            
            translate(colWidth)
            
    # augment page number
    pageNumber += 1

########
# Post #
########

# save PDF
savePath = plaintextPath.replace('.voiceLeading', '.pdf').replace('voiceLeading', 'pdf')
saveImage(savePath)