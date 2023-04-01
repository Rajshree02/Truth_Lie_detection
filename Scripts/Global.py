
#FOLDER PATHS
frameFolderPath = "./input/frames/"
videoOutputFolderPath = "D:/projects/kleosHackathon/streamlitFrontend/output/videos/"
audioOutput = "D:/projects/kleosHackathon/streamlitFrontend/generateVideos/outputAudio/output.wav"
videoInputFolderPath = "D:/projects/kleosHackathon/streamlitFrontend/input/videos"

thresholdFramesFolderPath = "D:/projects/kleosHackathon/streamlitFrontend/generateVideos/thresholdFrames/"

#THRESHOLDS
aspectRatioThreshold = 0.15
eyeGazeThreshold = 4.0
lipContractionRatio = .27



numberOfFrames = 0


def restartGlobals():
    numberOfFrames = 0

