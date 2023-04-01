import streamlit as st
import os, sys
from Scripts import Global
from generateVideos import generateVideos
from vosk import Model, KaldiRecognizer, SetLogLevel

# model = None

# model_path = "D:/projects/kleosHackathon/streamlitFrontend/generateVideos/model/vosk-model-en-us-0.22/vosk-model-en-us-0.22"
# # path to vosk model downloaded from
# # https://alphacephei.com/vosk/models
# if not os.path.exists(model_path):
#     print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as {model_path}")
#     sys.exit()

# def loadModel():
#     global model
#     print(f"Reading your vosk model '{model_path}'...")
#     model = Model(model_path)
#     print(f"'{model_path}' model was successfully read")

with st.spinner('loading model...'):
    # generateVideos.segmentVideos(filename)
    generateVideos.loadModel()

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

filename = file_selector(Global.videoInputFolderPath)

st.write('You selected `%s`' % os.path.abspath(filename))

if st.button('Click to preprocess'):
    generateVideos.segmentVideos(os.path.abspath(filename))
    st.success("done")



