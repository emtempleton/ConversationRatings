#Continuous Conversation Ratings
#Emma Templeton (12/2016)

#TASK: Displays instructions to participants, gives them a chance to practice using
#the slider bar, then plays conversation video. Participants move the mouse to report
#how connected they felt to their study partner. Script queries and records mouse 
#position every 0.1 seconds.

#Current Flaws:
#1. Lag between first practice video and next screen. I believe it has something to do 
#   with the size of the second video, as this doesn't happen when I used smaller, test
#   videos. As a bandaid, I've added a screen that says "reponses are recording" so participants
#   have something to look at during this lag.

#2. The timing could be improved. I used a hack-y clock-based way to record slider position
#   every 0.1 seconds, though there is drift. I think it'd be better to use a frame-based
#   system, though I'm unsure how to implement and whether I would run into issues running
#   the same script on multiple machines.

#3. The script periodically crashes, giving the error "Fatal Python error: (pygame parachute) Segmentation Fault"
#   My hunch is that certain functions are using pygame rather than pyglet, the former of which
#   is no longer being developed. I tried to set my window as as winType = 'pyglet' but still get
#   this error occassionally. 

#4. Not a flaw, but just a heads up that I'd like to export each rating to the .csv file on
#   the fly, in case the program crashes mid-video. Currently, if this happens, no data is 
#   saved. Adding this step into the loop might make the timing worse. 

#########################################
#import stuff
from __future__ import absolute_import, division
from psychopy import locale_setup, gui, visual, core, data, event, logging, sound
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import os
import sys
import numpy as np
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import psychopy.core

#########################################

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

#input subject and partner ID; store values for later
gui=psychopy.gui.Dlg() 
gui.addField("Subject ID: ")
gui.addField("Partner ID: ")
gui.show()
subID=gui.data[0]
partnerID=gui.data[1]

dir= './data/'+str(subID)+'_'+str(partnerID)+'.csv'
while os.path.exists(dir): #if path exists, remame it to avoid overwriting data
    print "CHECK SUBJECT NUMBER"
    newSubID = subID+"000"
    dir = './data/'+str(newSubID)+'_'+str(partnerID)+'.csv'

#########################################
#SETUP: DEFINE WINDOW

#Window
win=psychopy.visual.Window(size=[1280, 800], units="pix", fullscr=False, color=[-1, -1, -1], winType='pyglet')

#Define screen center
cX=0
cY=0

videoX=cX
videoY=cY+50
#########################################
#DRAW SCALE

mouse = psychopy.event.Mouse(visible=False,newPos=[0,-200], win=win)

#Draw Rating scale
scaleX=cX
scaleY=cY-200
ratingScaleWidth=480
ratingScaleHeight=1
ratingScale = psychopy.visual.Rect(win, width=ratingScaleWidth, height=ratingScaleHeight, pos=[scaleX,scaleY])

sliderLeftEnd = -240
sliderRightEnd = 240

#Draw Slider Handle 
handleWidth=1
handleHeight=20
handle = psychopy.visual.Rect(win, width=handleWidth, height=handleHeight, pos=[scaleX,scaleY])

#Draw Labels
label1X=-240
label1Y=scaleY-25
label1_txt="None"
label1=psychopy.visual.TextStim(win=win, alignHoriz='center', text=label1_txt, color=[1, 1, 1], height=20, pos=[label1X,label1Y])

label2X=240
label2_txt="Very"
label2=psychopy.visual.TextStim(win=win, alignHoriz='center', text=label2_txt, color=[1, 1, 1], height=20, pos=[label2X,label1Y])

#Draw Title
title_txt="How connected did you feel at this moment?"
titleY=videoY+225
title=psychopy.visual.TextStim(win=win, alignHoriz='center', text=title_txt, color=[1, 1, 1], height=25, pos=[cX,titleY], wrapWidth=550)

#########################################
#advance instructions
advance_txt="Press any key to continue"
advance=psychopy.visual.TextStim(win=win, alignHoriz='center', text=advance_txt, color=[1, 1, 1], height=30, pos=[0,-250], wrapWidth=1000)

#instruction text
instr1="You will be watching the video-taped conversation that you just had. As you watch, think back to how you were feeling during that conversation."
instr2="Your task is to report how connected you felt to your study partner over the course of your conversation. You will make these ratings by moving the computer mouse." 
instr3="These ratings will not be shared with your study partner. Please do your best to accurately report how connected you felt to your study partner at each point in time."

instruct1=psychopy.visual.TextStim(win=win,alignHoriz='left',text=instr1,color=[1, 1, 1],height=30,pos=[-500,250],wrapWidth=1000)
instruct2=psychopy.visual.TextStim(win=win,alignHoriz='left',text=instr2,color=[1, 1, 1],height=30,pos=[-500,100],wrapWidth=1000)
instruct3=psychopy.visual.TextStim(win=win,alignHoriz='left',text=instr3,color=[1, 1, 1],height=30,pos=[-500,-50],wrapWidth=1000)

practice_txt = "Before watching the conversation, take some time to familiarize yourself with the rating scale. Move the mouse to move the slider."
practice=psychopy.visual.TextStim(win=win,alignHoriz='left',text=practice_txt,color=[1, 1, 1],height=30,pos=[-500,250],wrapWidth=1000)

reminder_txt = "Press the space bar once you feel comfortable using this slider"
reminder=psychopy.visual.TextStim(win=win,alignHoriz='center',text=reminder_txt,color=[1, 1, 1],height=20,pos=[0,0],wrapWidth=400)

#########################################
#LOAD VIDEOS

#Loading Screen
load="Video is loading. This may take several minutes."
text=psychopy.visual.TextStim(win=win, alignHoriz='center', text=load, color=[1, 1, 1], height=30, wrapWidth=1000)
text.draw()
win.flip()

#Loaded Screen
load="Video has loaded!"
text2=psychopy.visual.TextStim(win=win, alignHoriz='center', text=load, color=[1, 1, 1], height=30, wrapWidth=1000)

#Define videos
#Videos are named / loaded based on subID and partnerID
videoFile = './videos/subs'+str(subID)+'_'+str(partnerID)+'.mov'
if not os.path.exists(videoFile): #allow flexibility for subID order
    videoFile = './videos/subs'+str(partnerID)+'_'+str(subID)+'.mov'
#videoFile = './videos/test.mov' #to test script with smaller video
practiceVideo = './videos/test.mov'

#Load Conversation Video
mov = visual.MovieStim3(win, videoFile, size=(480, 360),
    flipVert=False, flipHoriz=False, pos=[videoX,videoY], loop=False)

#Load Practie Video
movPractice = visual.MovieStim3(win, practiceVideo, size=(480, 360),
    flipVert=False, flipHoriz=False, pos=[videoX,videoY], loop=False)

#Alert experimeter that the videos have been loaded
if mov.duration > 0:
    text2.draw()
    win.flip()
    psychopy.event.waitKeys(keyList=['space'])


#########################################
#INSTRUCTIONS
instruct1.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct1.draw()
instruct2.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

instruct1.draw()
instruct2.draw()
instruct3.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#PRACTICE TRIALS 
practice.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#PRACTICE TRIALS 
ratingScale.setAutoDraw(True)
handle.setAutoDraw(True)
label1.setAutoDraw(True)
label2.setAutoDraw(True)
title.setAutoDraw(True)

oldMouseX = 0

#play practice video
while movPractice.status != visual.FINISHED:
    movPractice.draw()
    win.flip()
       
    mouseRel=mouse.getRel()
    mouseX=oldMouseX + mouseRel[0]
    if mouseX > 240:
     mouseX = 240
    if mouseX < -240:
     mouseX = -240
    handle.setPos([mouseX, scaleY])
    handle.draw()
    oldMouseX=mouseX

    if event.getKeys(['space']):
        #everything before "break" is just to give participants something
        #to look at during the weird lag
        win.flip()

        ratingScale.setAutoDraw(False)
        handle.setAutoDraw(False)
        label1.setAutoDraw(False)
        label2.setAutoDraw(False)
        title.setAutoDraw(False)
        fillerTxt="Responses are being recorded"
        filler=psychopy.visual.TextStim(win=win, alignHoriz='center', text=fillerTxt, color=[1, 1, 1], height=30, wrapWidth=1000)
        filler.draw()
        break

#replace practice video with instructions
while movPractice.status == visual.FINISHED:
    reminder.draw()
    win.flip()
    
    mouseRel=mouse.getRel()
    mouseX=oldMouseX + mouseRel[0]
    if mouseX > 240:
     mouseX = 240
    if mouseX < -240:
     mouseX = -240
    handle.setPos([mouseX, scaleY])
    handle.draw()
    oldMouseX=mouseX

    if event.getKeys(['space']):
        #everything before "break" is just to give participants something
        #to look at during the weird lag
        win.flip()

        ratingScale.setAutoDraw(False)
        handle.setAutoDraw(False)
        label1.setAutoDraw(False)
        label2.setAutoDraw(False)
        title.setAutoDraw(False)
        fillerTxt="Responses are being recorded"
        filler=psychopy.visual.TextStim(win=win, alignHoriz='center', text=fillerTxt, color=[1, 1, 1], height=30, wrapWidth=1000)
        filler.draw()
        break

win.flip()

ratingScale.setAutoDraw(False)
handle.setAutoDraw(False)
label1.setAutoDraw(False)
label2.setAutoDraw(False)
title.setAutoDraw(False)

#########################################
#POST-PRACTICE SCREEN

mouse = psychopy.event.Mouse(visible=False, win=win)

practice_txt2 = "Now that you are familiar with the rating scale, it's time to start the task! Remember to move the slider to accurately report how connected you felt to your study partner at each moment in time. The video will play immediately after this screen."
practice2=psychopy.visual.TextStim(win=win,alignHoriz='left',text=practice_txt2,color=[1, 1, 1],height=30,pos=[-500,250],wrapWidth=1000)

practice2.draw()
advance.draw()
win.flip()
psychopy.event.waitKeys()

#########################################
#INITIALIZE VARIABLES

ratingScale.setAutoDraw(True)
handle.setAutoDraw(True)
label1.setAutoDraw(True)
label2.setAutoDraw(True)
title.setAutoDraw(True)
mov.setAutoDraw(True)

timeAtLastRecord = 0
TIME_INTERVAL = 0.1 #how frequently to sample / record scale responses
oldMouseX = 0 #mouse position in x-axis
ratings = [] #to store continous ratings
timePerRating = [] #matches ratings with time

#set clock
clock = core.Clock()

while mov.status != visual.FINISHED:
    timeToRecord = clock.getTime() 
       
    mouseRel=mouse.getRel()
    mouseX=oldMouseX + mouseRel[0]
    if mouseX > 240:
     mouseX = 240
    if mouseX < -240:
     mouseX = -240
    handle.setPos([mouseX, scaleY])
    handle.draw()
    oldMouseX=mouseX
    
    #hacky way to improve timing. account for time it takes to perform above steps.
    m_t2 = clock.getTime()
    elapsed2 = m_t2 - timeToRecord
    timeToRecord = timeToRecord - elapsed2
           
    #query and record rating info every 0.1 seconds
    if (timeToRecord - timeAtLastRecord) > TIME_INTERVAL:
     sliderValue = (mouseX - sliderLeftEnd) / (sliderRightEnd - sliderLeftEnd) * 100
     ratings.append(round(sliderValue,0))
     timePerRating.append(round(timeToRecord,2))
     
     #hacky way to improve timing. account for time it takes to perform above steps.
     m_t = clock.getTime()
     elapsed = m_t - timeToRecord
     timeAtLastRecord = timeToRecord - elapsed
     
    win.flip() 

    if event.getKeys(['escape']):
        break

#########################################
#RECORD AND SAVE RELEVANT INFO

#record time and value 
numRows = len(ratings)
subCol = [subID] * numRows
partnerCol = [partnerID] * numRows
dataFrame = np.c_[subCol, partnerCol, ratings, timePerRating]

#save ratings
#will want to do this on the fly eventually
fmt='%s,%s,%s,%s'
np.savetxt(
    dir, 
    dataFrame, 
    delimiter=",",
    fmt=fmt,
    header="SubID, PartnerID, Rating, Time"
)

#########################################
#Alert participants that they are done with the task

win.flip()

ratingScale.setAutoDraw(False)
handle.setAutoDraw(False)
label1.setAutoDraw(False)
label2.setAutoDraw(False)
title.setAutoDraw(False)
mov.setAutoDraw(False)

end_txt = "You are all done with this task! Please open the door to alert the experimenter and then remain seated until they arrive."
end=psychopy.visual.TextStim(win=win,alignHoriz='center',text=end_txt,color=[1, 1, 1],height=30,pos=[0,0],wrapWidth=1000)

end.draw()
win.flip()
psychopy.event.waitKeys(keyList=['escape'])

#########################################
#SHUT DOWN

win.close()
core.quit()
