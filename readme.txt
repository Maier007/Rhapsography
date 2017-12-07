##########################
###    RHAPSOGRAPHY    ###
##########################

Modules/Libraries to setup
 - numpy (using pip install)
 - EasyMIDI (download from website and simply import)
 - openCV (follow online directions for correct version of python)
 - pygame (install with pip)
 - download haarcascade xml files from online

##########################
This is an experimental program that attempts to connect music and mood through 
a program using machine learning.  To generate music, the program creates random 
music and judges the music based on the pitch jumps in melody.  The data stored 
in musicData1.py is used to judge what is closest to newly, randomly generated 
music.  The music is regenerated until the mood detected matches the mood goal.  
Volume was somewhat hardcoded, as well as the first chord in the chord progression 
must be roman chord I.  Also, the scale that the melody comes from never changes, 
and the length of the music is four bars.  
Minor/major key relating to mood was never hardcoded, though much of the sad and
powerful music is minor key, and happy and peaceful music tend to be in major key.  

Users can either simply select a mood or they may use openCV to detect the mood.  
This is done by detecting a smile, and if there is a smile, and if teeth are showing, 
the smile is happy.  If no teeth are showing, the smile is simply peaceful.  With
no smile, the program relies on the position of the eyes, where if the eyes are in
the upper half of the screen, pride and power are sensed, whereas if the eyes are in
the lower half, sadness is sensed.  
##########################