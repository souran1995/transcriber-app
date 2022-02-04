import streamlit as st
import os
import sys
import time
import requests
from zipfile import ZipFile
from dotenv import load_dotenv

def get_url(token,data):
  '''
    Parameter:
      token: The API key
      data : The File Object to upload
    Return Value:
      url  : Url to uploaded file
  '''
  headers = {'authorization': token}
  response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=data)
  url = response.json()["upload_url"]
  print("Uploaded File and got temporary URL to file")
  return url

def get_transcribe_id(token,url):
  '''
    Parameter:
      token: The API key
      url  : Url to uploaded file
    Return Value:
      id   : The transcribe id of the file
  '''
  endpoint = "https://api.assemblyai.com/v2/transcript"
  json = {
    "audio_url": url
  }
  headers = {
    "authorization": token,
    "content-type": "application/json"
  }
  response = requests.post(endpoint, json=json, headers=headers)
  id = response.json()['id']
  print("Made request and file is currently queued")
  return id

def upload_file(fileObj):
  '''
    Parameter: 
      fileObj: The File Object to transcribe
    Return Value:
      token  : The API key
      transcribe_id: The ID of the file which is being transcribed
  '''
  #load_dotenv()
  api_key = 'acdd78a619a34a9cb7cde9ac80cc3b03'

  token = 'acdd78a619a34a9cb7cde9ac80cc3b03'
  file_url = get_url(token,fileObj)
  transcribe_id = get_transcribe_id(token,file_url)
  return token,transcribe_id

def get_text(token,transcribe_id):
  '''
    Parameter: 
      token: The API key
      transcribe_id: The ID of the file which is being 
    Return Value:
      result : The response object
  '''  
  endpoint = f"https://api.assemblyai.com/v2/transcript/{transcribe_id}"
  headers = {
    "authorization": token
  }
  result = requests.get(endpoint, headers=headers).json()
  return result

def app():
        st.subheader("Audio_to_Text")  
        fileObject = st.file_uploader(label = "Please upload your file" )

        if fileObject:
                token, t_id = upload_file(fileObject)
                result = {}
                #polling
                sleep_duration = 1
                percent_complete = 0
                progress_bar = st.progress(percent_complete)
                st.text("Currently in queue")
                while result.get("status") != "processing":
                        percent_complete += sleep_duration
                        time.sleep(sleep_duration)
                        progress_bar.progress(percent_complete/10)
                        result = get_text(token,t_id)

                sleep_duration = 0.01

                for percent in range(percent_complete,101):
                        time.sleep(sleep_duration)
                        progress_bar.progress(percent)

                with st.spinner("Processing....."):
                        while result.get("status") != 'completed':
                                result = get_text(token,t_id)

                st.balloons()
                st.header("Transcribed Text")
                st.subheader(result['text'])