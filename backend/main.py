from fastapi import FastAPI, Request, File, UploadFile
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import numpy as np
import io
import cv2
import shutil
import pytesseract
import requests
import uvicorn

import config
import inference

app = FastAPI()

@app.post("/")
async def root(file: UploadFile = File(...)):
	with open(f'{file.filename}', "wb") as buffer:
		shutil.copyfileobj(file.file, buffer)
	return {"file_name": file.filename}

def upload_file(filename):
 
  #load_dotenv()
  model = 'acdd78a619a34a9cb7cde9ac80cc3b03'

  token = 'acdd78a619a34a9cb7cde9ac80cc3b03'
  file_url = inference(token,filename)
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


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)