# Importing all necessary libraries
import cv2
import os
from Scripts import Global

# Read the video from specified path


# try:
# 	# creating a folder named data
# 	if not os.path.exists('lie_frames'):
# 		os.makedirs('lie_frames')

# if not created then raise error
# except OSError:
# 	print ('Error: Creating directory of data')

# frame

def makeFrames(filePath):
    currentframe = 0
    currentVideo = 0
    # for i in os.listdir(Global.videoOutputFolderPath):
    # cam = cv2.VideoCapture(Global.videoOutputFolderPath+"output"+str(currentVideo)+".mp4")
    cam = cv2.VideoCapture(filePath)
    while(True):
        
        # reading from frame
        ret,frame = cam.read()

        if ret:
            # if video is still left continue creating images
            name = Global.frameFolderPath + str(currentframe) + '.jpg'
            print ('Creating...' + name)

            # writing the extracted images
            cv2.imwrite(name, frame)

            # increasing counter so that it will
            # show how many frames are created
            currentframe += 1
        else:
            break

    # Release all space and windows once done
    cam = None
    currentVideo+=1

    Global.numberOfFrames = currentframe



