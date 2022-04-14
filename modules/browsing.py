from selenium import webdriver
from selenium.webdriver.common.by import By
import time

from settings import *


class PageDriver :
    def __init__(self) :
        self.browser = webdriver.Firefox(executable_path=PATH_GECKODRIVER)

    def _load_page(self, url) :
        self.browser.get(url)
        self._delay()

    def _delay(self) :
        time.sleep(1)

    def authenticate(self, user, passw) :
        self._load_page(SPOTIFY_LOGIN)

        user_input = self.browser.find_element(By.ID, "login-username")
        passw_input = self.browser.find_element(By.ID, "login-password")
        user_input.send_keys(user)
        passw_input.send_keys(passw)
        
        self.browser.find_element(By.XPATH, LOGIN_BUTTON).click()
        self._delay() #Button refers to an link, site has to load again
        
    def get_playlist_tags(self) :
        playlist_urls = []

        self._load_page(SPOTIFY_URL)
        playlist_elements = self.browser.find_elements(By.CLASS_NAME, PLAYLIST_TAG)
        for element in playlist_elements :
            url = element.get_attribute("href")
            if url:
                playlist_urls.append(url)
        return playlist_urls

    def get_playlist_content(self, url) :
        playlist_content = []
        self._load_page(url)
        song_info = self.browser.find_elements(By.CLASS_NAME, SONG_NAME_TAG)

        for i in range(0, len(song_info), 2) :
            print(song_info[i].text)
            #playlist_content.append(Song(name, interpreter, ""))

        return playlist_content

      


class SpotifyFront :
    def __init__(self, user, passw) :
        self.driver = PageDriver()
        self.driver.authenticate(user, passw)

    def load_playlists(self) :
        playlist_urls = self.driver.get_playlist_tags()
        content = self.driver.get_playlist_content(playlist_urls[0])

        for song in content :
            pass
            #print(song)



class Song :
    def __init__(self, name, interpreter, thumbnail_url) :
        self.name = name
        self.interpreter = interpreter
        self.thumbnail_url = thumbnail_url

    def __repr__(self) :
        return f'Song "{self.name}" from "{self.interpreter}"'