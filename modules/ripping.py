
#from browsing import Song


from concurrent.futures import thread
import string
import yt_dlp
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
from urllib import request
import os
from settings import *
from modules.calcfunc import convert_duration
from string import punctuation
import threading

#
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import Keys

#https://stackoverflow.com/questions/6893968/how-to-get-the-return-value-from-a-thread-in-python
class ThreadWithResult(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}, *, daemon=None):
        def function():
            self.result = target(*args, **kwargs)
        super().__init__(group=group, target=function, name=name, daemon=daemon)

class get_url_using_name:

    def thread_example(self):
        print("Thread running")
        return "Thread ran"

    def __init__(self,song):
        self.song = song
        self.songname, self.interpreter = song.get_information()
        self.name = self.songname+" " +self.interpreter
        self.supposed_duration = song.get_duration()
        #self.supposed_duration = "2:50"
        #self.name = name
        print(self.name, self.interpreter)

    def start_selenium(self, name):
        #options = Options()
        #options.headless = True
        
        browser = webdriver.Firefox(executable_path="./drivers/geckodriver.exe")
        browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't') 
        browser.get(self.youtube_url)

        #time.sleep(10)

        #consent_button_css = 'ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)'
        #consent= browser.find_element_by_css_selector(consent_button_css)
        #consent.click()
        WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'ytd-button-renderer.style-scope:nth-child(2) > a:nth-child(1) > tp-yt-paper-button:nth-child(1)'))).click()
        time.sleep(3)
        #time.sleep(1)
        content = browser.page_source.encode('utf-8').strip()
        print(f'content:{content[:100]}')


        soup = BeautifulSoup(content, 'lxml')


        try:
            titles = soup.find_all('a',id='video-title')
            durations = soup.find_all('span', id='text')
            href_links = [video.get_attribute('href') for video in browser.find_elements_by_id("thumbnail")]
            dump_variable = href_links[0]
        except:
            try:
                time.sleep(5)
                titles = soup.find_all('a',id='video-title')
                durations = soup.find_all('span', id='text')
                href_links = [video.get_attribute('href') for video in browser.find_elements_by_id("thumbnail")]
            except:
                time.sleep(5)
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
            print(f"duration:{duration_cut_completely}---")
            
            if duration_cut_completely == 'SHORTS':
                continue
            offset_durations = abs(self.supposed_duration-convert_duration(duration_cut_completely))
            
            if offset_durations < 3:
                #correct_video_title = titles[counter].text.replace("\n","")
                print(f"FOUND CORRECT VIDEO! {titles[counter].text}, {duration_cut_completely}url:{href_links[counter]}")
                download_url.append(href_links[counter]) #+1

                counter +=1
        print(f"download_url:{download_url}")
        
        #close browser
        browser.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

        if type(download_url[0]) == string:
            return download_url[0]
        else:
            return download_url[1]


    def threading_(self, how_many_threads, target_function, arguments):
        print("start of threading",how_many_threads)
        thread_names = []
        for number in range(how_many_threads):
            thread_names.append(f"Thread_{number}")
            print(f"thread_names:{thread_names}")

        for i in range(len(thread_names)):
            print(f"thread_names:{thread_names[i]}")
            thread_names[i] = threading.Thread(target=target_function, args=arguments)
            thread_names[i].start()
            #thread_names[i].join()
            #print(thread_names[i].result)
            #thread_names[i].terminate()
            

                

    def find_by_artist_url(self):
        
        pass
    
        
    def create_youtube_url(self):

        for char in punctuation:
            url_attachment = self.name.replace(char,"")
            
        prefix = "https://www.youtube.com/results?search_query="
        youtube_url = prefix+url_attachment
        print(f"youtube_url:{youtube_url}")

        self.youtube_url = youtube_url
        
        return youtube_url
        


class Rip():
    from yt_dlp import YoutubeDL
    yt = YoutubeDL()
    def download_opus(self, url,name):
        """
        #dummy_song = Song("DummyName", "DummyInterpreter", "DummyUrl")
        settings = YT_DLP_OPTIONS
        settings['outtmpl'] = OUTPUT_DIR+name
        with yt_dlp.YoutubeDL(YT_DLP_OPTIONS) as ydl:
            ydl.download([url])
        """
        os.chdir(OUTPUT_DIR)
        os.system(f'yt-dlp --extract-audio --audio-format mp3 --audio-quality 0 {url}')
        os.chdir('..')
    def download_url_list(self, url,name):
        self.download_opus(url,name)
            



#g1 = get_url_using_name()
#g1.create_youtube_url()
#download_url = g1.start_selenium()

#r1 = Rip()
#r1.download_url_list(download_url)



#print(f"downloadurl:{download_url}")



"""extract youtube video with highest quality
yt-dlp --extract-audio --audio-format mp3 --audio-quality 0
"""