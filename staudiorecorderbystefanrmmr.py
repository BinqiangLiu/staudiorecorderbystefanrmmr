# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023
#https://github.com/stefanrmmr/streamlit_audio_recorder

import streamlit as st
from st_custom_components import st_audiorec
from io import BytesIO
import openai
#import pyttsx3
#import sounddevice as sd
import soundfile as sf
import numpy as np
# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

system_message=""
transcript=""

# Global variable to hold the chat history, initialize with system role
conversation = [{"role": "system", "content": "You are an intelligent professor."}]
#******************

# DESIGN implement changes to the standard streamlit UI/UX
# --> optional, not relevant for the functionality of the component!
st.set_page_config(page_title="streamlit_audio_recorder")
# Design move app further up and remove top padding
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''',
            unsafe_allow_html=True)
# Design change st.Audio to fixed height of 45 pixels
st.markdown('''<style>.stAudio {height: 45px;}</style>''',
            unsafe_allow_html=True)
# Design change hyperlink href link color
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # darkmode
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''',
            unsafe_allow_html=True)  # lightmode
   # TITLE and Creator information
st.title('by Stefan streamlit audio recorder')
audio = st_audiorec() # tadaaaa! yes, that's it! :D
audio_type = type(audio)
print(audio_type)
st.write(audio_type)

if audio is not None:
    # To play audio in frontend:
    st.write("你输入的语音")
    st.audio(audio.tobytes())    
    # To save audio to a file:/可以视为是临时文件，就是用于语音转文本用
    audio_file = open("audiorecorded.wav", "wb")    
    audio_file.write(audio.tobytes())
    audio_file.close()
    with open("audiorecorded.wav", "rb") as sst_audio_file:
        transcript = openai.Audio.transcribe(
            file = sst_audio_file,
            model = "whisper-1",
            response_format="text"        
        )
    print("Transcript of your questions:",  transcript)
    st.write("Transcript of your questions:",  transcript)
#    print("Transcript of your questions:",  transcript["text"])

#   ChatGPT API
#   append user's inut to conversation
    conversation.append({"role": "user", "content": transcript})
#    conversation.append({"role": "user", "content": transcript["text"]})
    
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=conversation
    )    
    print(response)

#   system_message is the response from ChatGPT API
    system_message = response["choices"][0]["message"]["content"]

#   append ChatGPT response (assistant role) back to conversation
    conversation.append({"role": "assistant", "content": system_message})

# Display the chat history
    st.header("你和AI的问答文字记录")
    st.write("你的提问（语音转文字）: " + transcript)
#    st.write("你的提问（语音转文字）: " + transcript["text"])
    st.write("AI回答（文字）: " + system_message)
    st.header("第二步：语音播放AI的回答")
    language = detect(system_message)
    st.write("检测到输出语言:", language)
    print(language)

def text_to_speech(text):
    try:
        tts = gTTS(text, lang=language, slow=False)
        tts.save("translationresult.mp3")
        st.write("Success TTS成功将AI回答转换为语音")
        return "Success TTS成功将AI回答转换为语音"    
    except Exception as e:
        # Handle the error, e.g., print an error message or return a default text
        print(f"Translation error: {e}")
        st.write("TTS RESULT ERROR将AI回答转语音失败！")
        return "TTS RESULT ERROR将AI回答转语音失败！"
        st.stop()

if system_message is None:
    st.write("请先向AI提问！")    
    st.stop()
else: 
    st.write("你的提问（AI问答模型中的记录transcript）")
    st.write(transcript)
    st.write("AI回答")            
    ai_output_audio = text_to_speech(system_message)
    audio_file = open("translationresult.mp3", "rb")
    audio_bytes = audio_file.read()
    st.audio("translationresult.mp3")
    st.write(response)    
    st.write(system_message)    

