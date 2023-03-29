import phase1
import Global
import cv2
import mediapipe as mp


def setThresholds():

    parameterDict = {}

    for i in range(0, 5):
        imgPath = Global.path+str(i)+".jpg"
        img = cv2.imread(imgPath) 

        height, width, _ = img.shape

        mp_face_mesh = mp.solutions.face_mesh

        face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

        rgb_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = face_mesh.process(rgb_image)

        p1 = phase1.get_lip_ratio(result, height, width)
        p2 = phase1.eyeGaze(img, result)
        p3 = phase1.get_emotions(i)

        parameterDict[i] = [p1,p2,p3]        

    print(parameterDict[1])


setThresholds()