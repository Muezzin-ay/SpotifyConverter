
#from browsing import Song


import yt_dlp
"""Beatiful Soup for extracting finding the youtube url by name & interpreter"""
from bs4 import BeautifulSoup
import requests

class get_url_using_name():

    def __init__(self):
        name = "Dua Lipa New Rules Lyrics"
        self.name = name

    def find_by_artist_url(self):
        #getting the request
        raw_webpage = requests.get(self.youtube_url)

        #converting the text
        webpage = BeautifulSoup(raw_webpage.text, "html.parser")


    def create_youtube_url(self):
        url_attachment = self.name.replace(" ","+")
        prefix = "https://www.youtube.com/results?search_query="
        youtube_url = prefix+url_attachment
        print(f"youtube_url:{youtube_url}")

        self.youtube_url = youtube_url
        


class Rip():
    def download_opus(self):
        #dummy_song = Song("DummyName", "DummyInterpreter", "DummyUrl")
        print("hello world")   

    def start(self):
        self.download_opus()


g1 = get_url_using_name()
g1.create_youtube_url()
g1.find_by_artist_url()