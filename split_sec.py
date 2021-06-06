import cv2
import os
from os.path import isdir
listing = os.listdir(r'in/')
count=1
frameRate = 0.03
dir=f'out/Frames/{frameRate}'
if not isdir (dir):
    os.makedirs(dir)
for vid in listing:
    print(vid)
    vid = r"in/"+vid
    vidcap = cv2.VideoCapture(vid)
    def getFrame(sec):
        vidcap.set(cv2.CAP_PROP_POS_MSEC,sec*1000)
        hasFrames,image = vidcap.read()
        if hasFrames:
        
            out=f"{dir}/image"+str(count)+".jpg"
            print(222, out)
            cv2.imwrite(out, image) # Save frame as JPG file
        return hasFrames
    sec = 0
     # Change this number to 1 for each 1 second
    
    success = getFrame(sec)
    while success:
        count = count + 1
        sec = sec + frameRate
        sec = round(sec, 2)
        success = getFrame(sec)