from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from modules.calcfunc import convert_duration
from settings import *



class SpotifyFront :
    def __init__(self, user, passw) :
        self.driver = PageDriver()
        self.driver.authenticate(user, passw)

    def _load_playlists(self) :
        return self.driver.get_playlist_data()

    def choose_playlist(self) :
        names, urls = self._load_playlists()
        
        print("Choose one Playlist: ")
        for counter, name in enumerate(names) :
            print(f"{counter+1}) {name}")
        selected_index = self._confirm_input(len(urls))

        return urls[selected_index]
        
    def _confirm_input(self, max_possible) :
        while True :
            try :
                selected_index = int(input("Playlist Number>>"))
                if (selected_index >= 0 and selected_index <= max_possible) :
                    return selected_index -1
            except :
                pass

    def load_songs(self, playlist_url) :
        return self.driver.get_playlist_content(playlist_url)

            

class PageDriver :
    def __init__(self) :
        self.browser = webdriver.Firefox(executable_path=PATH_GECKODRIVER)

    def _load_page(self, url) :
        self.browser.get(url)
        self._delay()

    def _delay(self) :
        time.sleep(LOADING_DELAY)

    def authenticate(self, user, passw) :
        self._load_page(SPOTIFY_LOGIN)

        user_input = self.browser.find_element(By.ID, "login-username")
        passw_input = self.browser.find_element(By.ID, "login-password")
        user_input.send_keys(user)
        passw_input.send_keys(passw)
        
        self.browser.find_element(By.XPATH, LOGIN_BUTTON).click()
        self._delay() #Button refers to an link, site has to load again
        
    def get_playlist_data(self) :
        playlist_names = []
        playlist_urls = []

        self._load_page(SPOTIFY_URL)
        playlist_elements = self.browser.find_elements(By.CLASS_NAME, PLAYLIST_URL)
        for element in playlist_elements :
            playlist_names.append(element.text)
            url = element.get_attribute("href")
            if url:
                playlist_urls.append(url)

        return playlist_names[2:], playlist_urls #Alle names except first two -> create playlist and favorite songs

    def get_playlist_content(self, url) :
        playlist_content = []
        self._load_page(url)

        #Cover url
        cover_url_data = self.browser.find_elements(By.CLASS_NAME, SONG_COVER)
        cover_urls = [url.get_attribute("src") for url in cover_url_data[1:]]

        #Song lenght
        durations = []
        duration_data = self.browser.find_elements(By.CLASS_NAME, 'HcMOFLaukKJdK5LfdHh0')
        for duration in duration_data :
            text = duration.text
            if text != "" and text != "HINZUFÜGEN" :
                durations.append(text)

        #Song name and intepreter
        song_info = self.browser.find_elements(By.CLASS_NAME, SONG_NAME)

        #Creating song objects
        song_count = len(durations)
        for i in range(song_count) :
            song_data = song_info[i].text.split("\n")
            playlist_content.append(Song(song_data[0], song_data[1], durations[i], cover_urls[i]))
        
        return playlist_content



class Song :
    def __init__(self, name, interpreter, duration, cover_url) :
        self.name = name
        self.interpreter = interpreter
        self.duration = convert_duration(duration)
        self.cover_url = cover_url

        self._edit_cover_url()

    def __repr__(self) :
        return f'Song "{self.name}"({self.duration}) from "{self.interpreter}", Cover "{self.cover_url}"'

    def _edit_cover_url(self) : #Replace a url part for better image resolution
        self.cover_url = self.cover_url.replace("ab67616d00004851", "ab67616d00001e02")

    def get_cover_url(self) :
        return self.cover_url

    def get_information(self) :
        return self.name, self.interpreter, self.duration