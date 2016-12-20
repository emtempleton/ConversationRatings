#Continuous Conversation Ratings
#Emma Templeton (12/2016)

#automatic imports from 'builder' feature
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding

#imports from Daisy's code
#visual display
import psychopy.visual
# actions manipulating display
import psychopy.event
#gui is for saving data, apprebiation for graphic user interface, to attach the experiment to the file
import psychopy.gui
import os
import sys
import numpy as np
from random import randint
from random import shuffle
import psychopy.core

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#input subject and partner ID
#store values for later
gui=psychopy.gui.Dlg() 
gui.addField("Subject ID: ")
gui.addField("Partner ID: ")
gui.show()
subID=gui.data[0]
partnerID=gui.data[1]

dir="data"+str(subID)+"_"+str(partnerID)+".csv";
while os.path.exists(dir): #if path exists, remame it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    subID = subID+"000"
    dir = "data"+str(subID)+"_"+str(partnerID)+".csv"
    
#load video ########
#figure out a good naming convention to call them

#instruction window
win=psychopy.visual.Window(
    size=[1280, 800],
    units="pix",
    fullscr=False, 
    color=[-1, -1, -1]
)

#instruction text
instr="Rate how connected you felt to your conversation partner.\n\nPress any key to continue."
text=psychopy.visual.TextStim(
    win=win,
    alignHoriz='center',
    text=instr,
    color=[1, 1, 1],
    height=40,
    wrapWidth=1000
)
text.draw()
win.flip()
psychopy.event.waitKeys()

#Display Video
mov = visual.MovieStim3(win, '/Users/Emma/Dropbox/HaveAConversation!/test.mov', size=(480, 360),
    flipVert=False, flipHoriz=False, loop=False)
print('orig movie size=%s' % mov.size)
print('duration=%.2fs' % mov.duration)
globalClock = core.Clock()

#Display Rating Scale
#ratingScale = visual.RatingScale(win=win, marker='circle', size=1.0, pos=[0.0, -300], low=0, high=100, labels=['None, Very'], scale='How connected do you feel?', markerStart='50', showAccept=False)

#Draw Rating scale
ratingScaleWidth=480
ratingScaleHeight=1
ratingScale = psychopy.visual.Rect(win, width=ratingScaleWidth, height=ratingScaleHeight, pos=[0.0, -300])

sliderLeftEnd = -240
sliderRightEnd = 240

#Draw Slider Handle 
handleWidth=1
handleHeight=20
handle = psychopy.visual.Rect(win, width=handleWidth, height=handleHeight, pos=[0.0, -300])

#Grab Mouse Position and Update the Scale Accordingly
mouse = psychopy.event.Mouse(visible=True, newPos=None, win=win) 

#re-draw slider handle based on the change in x-axis
timeAtLastInterval = 0
TIME_INTERVAL = 0.05
oldMouseX = 0
ratings = []
timePerRating = []

while mov.status != visual.FINISHED:
    mov.draw()
    ratingScale.draw()
    handle.draw()
    win.flip()
    timeNow = globalClock.getTime()
    if (timeNow - timeAtLastInterval) > TIME_INTERVAL:
       mouseRel=mouse.getRel()
       mouseX=oldMouseX + mouseRel[0]
       if mouseX > 240:
        mouseX = 240
       if mouseX < -240:
        mouseX = -240
       handle = psychopy.visual.Rect(win, width=handleWidth, height=handleHeight, pos=[mouseX, -300])
       timeAtLastInterval = timeNow
       oldMouseX=mouseX
       sliderValue = (mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100
       handle.draw()
       ratings.append(round(sliderValue,0))
       timePerRating.append(round(timeNow,3))
    if event.getKeys():
        break

#record time and value (will need to do this inside the loop. will need a counter variable)
#create a matrix (same as before) within the loop, the save outside of the loop, along with subID etc.
numRows = len(ratings)
subCol = [subID] * numRows
partnerCol = [partnerID] * numRows
dataFrame = np.c_[subCol, partnerCol, ratings, timePerRating]

#save ratings 
fmt='%s,%s,%s,%s'
np.savetxt(
    dir, 
    dataFrame, 
    delimiter=",",
    fmt=fmt,
    header="SubID, PartnerID, Rating, Time"
)

win.close()
core.quit()

#TODO
#allow for large movie files
#re-draw and record / sample at different rates
#clean up variable names / file structure
#change timing to be frame-based (yes!)



