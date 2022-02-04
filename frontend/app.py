import streamlit as st
from pytube import YouTube
import os
import sys
import time
import requests
from zipfile import ZipFile
from PIL import  Image

# Custom imports 
from pages.multipage import MultiPage
import pages.Video_to_Text as Video_to_Text , pages.Video_Sound_to_Text as Video_Sound_to_Text , pages.Audio_to_Text as Audio_to_Text, pages.Online_video_to_Text as Online_video_to_Text

# Create an instance of the app 
app = MultiPage()

# Add all your application here
app.add_page("Video to Text", Video_to_Text.app)
app.add_page("Video sound to Text", Video_Sound_to_Text.app)
app.add_page("Audio to Text", Audio_to_Text.app)
app.add_page("Online Video to Text",Online_video_to_Text.app)

# The main app
app.run()
