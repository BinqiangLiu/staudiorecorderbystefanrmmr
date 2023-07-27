# streamlit_audio_recorder by stefanrmmr (rs. analytics) - version January 2023

import streamlit as st
from st_custom_components import st_audiorec

#******************
import streamlit as st
import openai
#import pyttsx3
import sounddevice as sd
import soundfile as sf
import numpy as np

# Load environment variables
from dotenv import load_dotenv
import os
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

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


def audiorec_demo_app():

    # TITLE and Creator information
    st.title('streamlit audio recorder')
    st.markdown('Implemented by '
        '[Stefan Rummer](https://www.linkedin.com/in/stefanrmmr/) - '
        'view project source code on '
        '[GitHub](https://github.com/stefanrmmr/streamlit_audio_recorder)')
    st.write('\n\n')

    # TUTORIAL: How to use STREAMLIT AUDIO RECORDER?
    # by calling this function an instance of the audio recorder is created
    # once a recording is completed, audio data will be saved to wav_audio_data

    wav_audio_data = st_audiorec() # tadaaaa! yes, that's it! :D

    if wav_audio_data is not None:
        # display audio data as received on the Python side
        col_playback, col_space = st.columns([0.58,0.42])
        with col_playback:
            st.audio(wav_audio_data, format='audio/wav')

#调用函数进行语音wav_audio_data转文字
    with st.spinner("Processing..."):
        text = transcribe_audio(wav_audio_data)
        response = chat_with_openai(text)

    # add some spacing and informative messages
    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')  # add vertical spacer
        st.write('\n')  # add vertical spacer
        st.write('The .wav audio data, as received in the backend Python code,'
                 ' will be displayed below this message as soon as it has'
                 ' been processed. [This informative message is not part of'
                 ' the audio recorder and can be removed easily] 🎈')

#******************
# Function to transcribe audio using OpenAI's Whisper API
# 定于使用OpenAI's Whisper API将语音转文字的函数
def transcribe_audio(wav_audio_data):
    audio_file = "audio_input.wav"
    sf.write(audio_file, wav_audio_data, 44100, format="wav")
    with open(audio_file, "rb") as file:
        transcript = openai.Audio.transcribe("whisper-1", file)
    os.remove(audio_file)  # Remove the temporary audio file
    return transcript["text"]

# Function to perform chat with OpenAI GPT-3
def chat_with_openai(input_text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": input_text}],
    )
    return response["choices"][0]["message"]["content"]

# Function to convert text to speech using pyttsx3
#def text_to_speech(text):
#    engine = pyttsx3.init()
#    engine.setProperty("rate", 150)
#    engine.setProperty("voice", "english-us")
#    engine.save_to_file(text, "response.mp3")
#    engine.runAndWait()
#    with open("response.mp3", "rb") as file:
#        response_audio = file.read()
#    os.remove("response.mp3")  # Remove the temporary audio file
#    return response_audio

# Main function to run the Streamlit app
# def main():
#     st.title("Audio to Chat App")

    # Audio input section
#     st.header("Step 1: Speak to the AI")
#     st.write("Click the 'Start Recording' button and speak to the AI.")
#******************


if __name__ == '__main__':
    # call main function
    audiorec_demo_app()
