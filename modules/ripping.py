
#from browsing import Song


import yt_dlp
from selenium import webdriver
from bs4 import BeautifulSoup
import time
from urllib import request
import os

class get_url_using_name:

    def __init__(self,song):
        self.song = song
        self.name, self.interpreter = song.get_information()
        name = "Harrison Heatwaves"
        self.supposed_duration = "2:50"
        self.name = name
        print(self.name, self.interpreter)

    def start_selenium(self):

        browser = webdriver.Firefox(executable_path="./drivers/geckodriver.exe")
        browser.get(self.youtube_url)

        time.sleep(10)
        consent_button_css = 'ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)'
        consent= browser.find_element_by_css_selector(consent_button_css)
        consent.click()
        
        content = browser.page_source.encode('utf-8').strip()



        soup = BeautifulSoup(content, 'lxml')



        titles = soup.find_all('a',id='video-title')
        durations = soup.find_all('span', id='text')
        href_links = [video.get_attribute('href') for video in browser.find_elements_by_id("thumbnail")]

        
        for href_link in href_links:
            #print(f"href:{href_link}")
            pass
        for title in titles:
            #print("title",title.text)
            pass
        counter = 0
        download_url = []
        for duration in durations:
            duration_cut = duration.text.replace(" ","")
            duration_cut_completely = duration_cut.replace("\n","")
            #print(f"duration:{duration}\n duration_cut:{duration_cut} \n duration_cut_completely:{duration_cut_completely}")
            #print(f"duration:{duration_cut_completely}---")
            
            if duration_cut_completely == self.supposed_duration:
                #correct_video_title = titles[counter].text.replace("\n","")
                print(f"FOUND CORRECT VIDEO! {titles[counter].text}, {duration_cut_completely}url:{href_links[counter+1]}")
                download_url.append(href_links[counter+1])

                counter +=1
        return download_url

                

    def find_by_artist_url(self):
        
        pass
    
        
    def create_youtube_url(self):
        url_attachment = self.name.replace(" ","+")
        prefix = "https://www.youtube.com/results?search_query="
        youtube_url = prefix+url_attachment
        print(f"youtube_url:{youtube_url}")

        self.youtube_url = youtube_url
        


class Rip():
    from yt_dlp import YoutubeDL
    yt = YoutubeDL()
    options = {
        'format':'bestaudio/best',
        'extractaudio':True,
        'audioformat':'mp3',
        'outtmpl':'/output/'+'%(id)s.%(ext)s',     #name the file the ID of the video
        'noplaylist':True,
        'nocheckcertificate':True,
        'proxy':"",
        'addmetadata':True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    def download_opus(self, url):
        #dummy_song = Song("DummyName", "DummyInterpreter", "DummyUrl")

        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download(["https://www.youtube.com/watch?v=pcnxkUbtJcE"])
           
    def download_url_list(self, download_url):
        for url in download_url:
            self.download_opus(url)
            



#g1 = get_url_using_name()
#g1.create_youtube_url()
#download_url = g1.start_selenium()

#r1 = Rip()
#r1.download_url_list(download_url)



#print(f"downloadurl:{download_url}")



"""extract youtube video with highest quality
yt-dlp --extract-audio --audio-format mp3 --audio-quality 0
"""