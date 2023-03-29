import streamlit as st
import os
from generateVideos import generateVideos
from vosk import Model, KaldiRecognizer, SetLogLevel
import sys
import pandas as pd
import numpy as np


#Scripts import
from Scripts import phase1


st.title("Truth-Lie-Detection")


model = None

model_path = "generateVideos/model/vosk-model-en-us-0.22/vosk-model-en-us-0.22"
# path to vosk model downloaded from
# https://alphacephei.com/vosk/models
if not os.path.exists(model_path):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
    sys.exit()


@st.cache_resource
def loadModel():
    global model
    print(f"Reading your vosk model '{model_path}'...")
    model = Model(model_path)
    print(f"'{model_path}' model was successfully read")
    return model

# model = loadModel() 

# with st.spinner('loading model...'):
#     # generateVideos.segmentVideos(filename)
#     loadModel()  

# video = st.file_uploader(label="upload video")

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector("input/videos")
st.write('You selected `%s`' % os.path.abspath(filename))

if st.button('Click to preprocess'):
    if filename.endswith((".mp4")):
        with st.spinner('Preprocessing the videos...'):
            # generateVideos.segmentVideos(filename)
            generateVideos.segmentVideos(os.path.abspath(filename), model)
        st.success('Done!')


# st.metric(label="Accuracy", value="90%", delta="Truth")



# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=['a', 'b', 'c'])

# st.area_chart(chart_data)


# chart_data = pd.DataFrame(
#     np.random.randn(20, 3),
#     columns=["a", "b", "c"])

# st.bar_chart(chart_data)

# emotion = phase1.get_emotion("./115.jpg", 115)


# st.write(emotion)

# st.write(phase1.get_emotions(115))

phase1.__main__()