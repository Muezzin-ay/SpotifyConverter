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

        cover_url_data = self.browser.find_elements(By.CLASS_NAME, SONG_COVER_TAG)
        cover_urls = [url.get_attribute("src") for url in cover_url_data[1:]]

        for counter, entry in enumerate(song_info) :
            song_data = entry.text.split("\n")
            playlist_content.append(Song(song_data[0], song_data[1], cover_urls[counter]))

        return playlist_content



class SpotifyFront :
    def __init__(self, user, passw) :
        self.driver = PageDriver()
        self.driver.authenticate(user, passw)

    def load_playlists(self) :
        playlist_urls = self.driver.get_playlist_tags()
        content = self.driver.get_playlist_content(playlist_urls[0])

        for song in content :
            print(song)



class Song :
    def __init__(self, name, interpreter, cover_url) :
        self.name = name
        self.interpreter = interpreter
        self.cover_url = cover_url

        self.edit_cover_url()

    def __repr__(self) :
        return f'Song "{self.name}" from "{self.interpreter}", Cover "{self.cover_url}"'

    def edit_cover_url(self) :
        self.cover_url = self.cover_url.replace("ab67616d00004851", "ab67616d00001e02")