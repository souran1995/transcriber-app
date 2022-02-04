import config
import cv2
import requests


def inference(model, data):
  
  headers = {'authorization': model}
  response = requests.post(config.UPLOAD_PATH,
                         headers=headers,
                         data=data)
  url = response.json()["upload_url"]
  
  return url


def get_transcribe_id(model,url):
 
  endpoint = config.TRANSCRIPT_PATH
  json = {
    "audio_url": url
  }
  headers = {
    "authorization": model,
    "content-type": "application/json"
  }
  response = requests.post(endpoint, json=json, headers=headers)
  id = response.json()['id']
  print("Made request and file is currently queued")
  return id
