import os
import sys
import wave
import json
from Scripts import Global

from vosk import Model, KaldiRecognizer, SetLogLevel
# !pip install vosk
from generateVideos import Word
import subprocess

from moviepy.editor import *

SetLogLevel(0)

# model = None

# model_path = "generateVideos/model/vosk-model-en-us-0.22/vosk-model-en-us-0.22"
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


def segmentVideos(videoFilePath, model):
    # name of the audio file to recognize
    audio_filename = Global.audioOutput
    # name of the text file to write recognized text
    # text_filename = "./audio/speech_recognition_systems_vosk_with_timestamps.txt"
    video_filename = videoFilePath

    output_folder_path = Global.videoOutputFolderPath


    cmd_str = "ffmpeg -i "+video_filename+" -acodec pcm_s16le -ac 1 -ar 8000 "+audio_filename+" -y"
    subprocess.call(cmd_str, shell=True)

    if not os.path.exists(audio_filename):
        print(f"File '{audio_filename}' doesn't exist")
        sys.exit()

    print(f"Reading your file '{audio_filename}'...")
    wf = wave.open(audio_filename, "rb")
    print(f"'{audio_filename}' file was successfully read")

    # check if audio is mono wav
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print("Audio file must be WAV format mono PCM.")
        sys.exit()


    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)


    results = []

    # recognize speech using vosk model
    while True:
        data = wf.readframes(8000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)

    part_result = json.loads(rec.FinalResult())
    results.append(part_result)

    # convert list of JSON dictionaries to list of 'Word' objects

    list_of_words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = Word.Word(obj)  # create custom Word object
            list_of_words.append(w)  # and add it to list

    nextTimestamps = []

    for idx, word in enumerate(list_of_words):
        if word.word == "next" and list_of_words[idx+1].word=="question":
            nextTimestamps.append(word)
            print(word.to_string())

    # forming a final string from the words
    text = ''
    for r in results:
        text += r['text'] + ' '

    print("\tVosk thinks you said:\n")
    print(text)

    clip = VideoFileClip(video_filename)
    # clip1 = clip.subclip(0,5)
    # clip1.write_videofile("outputSample.mp4")
    clipNum = 0

    clip1 = clip.subclip(0, nextTimestamps[0].end)
    clip1.write_videofile(output_folder_path+"/output"+str(clipNum)+".mp4")
    clipNum+=1

    for i in range(len(nextTimestamps)):
        clip = VideoFileClip(video_filename)
        if i != len(nextTimestamps)-1:
            clip1 = clip.subclip(nextTimestamps[i].start, nextTimestamps[i+1].start)
            clip1.write_videofile(output_folder_path+"/output"+str(clipNum)+".mp4")
            clipNum+=1
        else:
            clip1 = clip.subclip(nextTimestamps[i].start)
            clip1.write_videofile(output_folder_path+"/output"+str(clipNum)+".mp4")
            clipNum+=1