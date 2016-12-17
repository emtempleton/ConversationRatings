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
ratingScale = visual.RatingScale(win=win, marker='circle', size=1.0, pos=[0.0, -300], low=0, high=100, labels=['None, Very'], scale='How connected do you feel?', markerStart='50', showAccept=False)
#NEXT STEP: get history and save it in .csv before closing

while mov.status != visual.FINISHED:
    mov.draw()
    ratingScale.draw()
    win.flip()
    if event.getKeys():
        break

A = subID;
B = partnerID;
C = ratingScale.getRating();
D = ratingScale.getRT();
E = ratingScale.getHistory();

#reformat the getHistory value to save into a csv
rating = np.array(E)
print(rating)

#add other info. multiply subID and partnerID by len(E) and the use np.c_[E, newValues]
numRows = len(E)
subCol = [subID] * numRows
partnerCol = [partnerID] * numRows
rating2 = np.c_[subCol, partnerCol, rating]
print(rating2)


#save ratings 
fmt='%s,%s,%s,%s'
np.savetxt(
    dir, 
    rating2, 
    delimiter=",",
    fmt=fmt,
    header="SubID, PartnerID, Rating, Time"
)

win.close()
core.quit()

#TODO
#ratings with mouse, based on position (maybe use the GUI for help)
#allow for large movie files
#small analysis script that breaks all the ratings into the same length based on time
#then combines them all together
#clean up variable names / file structure



