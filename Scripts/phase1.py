import numpy as np
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import mediapipe as mp
import pandas as pd
import math
import os
from deepface import DeepFace

import streamlit as st

from Scripts import Global


path = Global.frameFolderPath

# img = cv2.imread(path+"120.jpg");

height = None
width = None


def dis(x,y):
    return math.dist(x,y)

def L_eye_gaze(img,gray):
    for facial_landmarks in gray.multi_face_landmarks:
        height, width, _ = img.shape
        pt1 = facial_landmarks.landmark[476]
        x1 = int(pt1.x * width)
        y1 = int(pt1.y * height)
        pt2= facial_landmarks.landmark[362]
        x2 = int(pt2.x * width)
        y2 = int(pt2.y * height)
#         print(dis((x1,y1),(x2,y2)))
        return dis((x1,y1),(x2,y2))

def R_eye_gaze(img,gray):
    for facial_landmarks in gray.multi_face_landmarks:
        height, width, _ = img.shape
        pt1 = facial_landmarks.landmark[474]
        x1 = int(pt1.x * width)
        y1 = int(pt1.y * height)
        pt2= facial_landmarks.landmark[263]
        x2 = int(pt2.x * width)
        y2 = int(pt2.y * height)
#         print(dis((x1,y1),(x2,y2)))
        return dis((x1,y1),(x2,y2))
    

def get_aspect_ratio(top, bottom, right, left):
    height=dis([top.x, top.y], [bottom.x, bottom.y])
    width=dis([right.x, right.y], [left.x, left.y])
    return height/width

def get_lip_ratio(result, height=height, width=width):
    for facial_landmarks in result.multi_face_landmarks:
        pt_bottom = facial_landmarks.landmark[17]
        x_bottom = int(pt_bottom.x * width)
        y_bottom = int(pt_bottom.y * height)
        pt_top = facial_landmarks.landmark[0]
        x_top = int(pt_top.x * width)
        y_top = int(pt_top.y * height)
        pt_left = facial_landmarks.landmark[61]
        x_left = int(pt_left.x * width)
        y_left = int(pt_left.y * height)
        pt_right = facial_landmarks.landmark[291]
        x_right = int(pt_right.x * width)
        y_right = int(pt_right.y * height)
        # aspect ratio
        h = math.dist((x_bottom, y_bottom),(x_top, y_top))
        w = math.dist((x_left, y_left),(x_right, y_right))
        return h/w
    

def eyeGaze(img, result):
    for facial_landmarks in result.multi_face_landmarks:
        pt1 = facial_landmarks.landmark[159]
        pt2 = facial_landmarks.landmark[145]
        pt3 = facial_landmarks.landmark[133]
        pt4 = facial_landmarks.landmark[33]
    if get_aspect_ratio(pt1, pt2, pt3, pt4) > Global.aspectRatioThreshold:
        x = L_eye_gaze(img, result)
        y = R_eye_gaze(img, result)

        return abs(x-y)
    
    return -1  


# truth data analysis
def get_emotion(img,i):
    
    p=path+str(i)+".jpg"

    img = cv2.imread(p);

   
    result=DeepFace.analyze(p,actions=('emotion'), silent=True)
    return result[0]['dominant_emotion']


def deleteFrames():
    for i in os.listdir(Global.frameFolderPath):
        os.remove(Global.frameFolderPath+i)


def __main__():
    global height, width

    #MODIFY THIS
    count = 0
    frameStart = 0

    parameterDict = {}

    for i in os.listdir(path):
        img = cv2.imread(path+str(count)+".jpg")
        height, width, _ = img.shape

        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)
        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_image)


        #0 - LIE
        #1 - TRUTH
        p1 = get_lip_ratio(result, height, width)
        if p1 > Global.lipContractionRatio:
            p1 = 1 
        else: 
            p1 = 0 

        
        p2 = eyeGaze(img, result)
        if p2 > Global.eyeGazeThreshold:
            p2 = 0 #Represents Lie
        else: 
            p2 = 1 #Represents Truth

        p3 = get_emotions(count)
        if p3 =="fear" or p3=="sad" or p3=="anger":
            p3 = 0 #Represents Lie
        elif p3=="neutral":
            p3 = 0.5 
        else:
            p3 = 1 #Represents Truth

        # st.write(p1, p2, p3)
        parameterDict[count- frameStart] = [p1,p2,p3]   

        count += 1 

    st.success("dict formed")
    print(parameterDict)
    giveResults(parameterDict)
        
        

def giveResults(parameterDict):
    c1 = 0
    c2 = 0
    c3 = 0
    for key in parameterDict.keys():
        c1 += parameterDict[key][0]
        c2 += parameterDict[key][1]
        c3 += parameterDict[key][2]

    c1 = (c1/Global.numberOfFrames) * 100
    c2 = (c2/Global.numberOfFrames) * 100
    c3 = (c3/Global.numberOfFrames) * 100
    
    # st.warning("RESULTS")
    # st.write(c1, c2, c3)

    st.warning("RESULTS IN PERCENTAGE OF TRUTH")
    st.write(c1, c2, c3)

    st.warning("AVERAGE")
    st.write("Percentage truth"+str((c1+c2+c3)/3))




def get_emotions(frameNo):
    # lst=[]
    # count=115
    # for i in os.listdir(path):
    result=DeepFace.analyze(path+str(frameNo)+'.jpg',actions=('emotion'))
    # count=count+1
    # print(result[0]['dominant_emotion'])
    return result[0]['dominant_emotion']
    # emotion=pd.DataFrame(lst,columns=["type"])
    # pd.value_counts(emotion["type"]).plot.bar()
    
# emotion=get_emotion(img,120)
# print(emotion)