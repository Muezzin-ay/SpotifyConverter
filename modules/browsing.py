from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from modules.calcfunc import convert_duration
from settings import *



class SpotifyFront :
    def __init__(self, login_data) :
        self.driver = PageDriver()
        user, passw = login_data
        self.driver.authenticate(user, passw)

    def get_playlist_links(self) :
        links = []
        elements = self.driver.search([PLAYLIST_URL], min_count=3)[0][2:]
        for data in elements :
            links.append(data.get_attribute('href'))
        return links

    def get_song_count(self, url) :
        print("sus")
        self.driver.load_page(url)
        print(self.driver.find_element(By.CLASS_NAME, 'Type__TypeElement-goli3j-0 ebHsEf').text)

    def get_playlist(self, url) :
        elements = self.driver.search(SONG_BLUEPRINT, url=url)
        url_elements = elements[1]
        cover_urls = [url.get_attribute("src") for url in url_elements[1:]]

        unfiltered = [duration.text for duration in elements[2]]
        durations = list(filter(lambda text: text != "" and text != "HINZUFÜGEN", unfiltered))

        name_elements = elements[0]
        names = [data.text.split("\n")[0] for data in name_elements]
        interpreters = [data.text.split("\n")[1] for data in name_elements]

        playlist = [Song(names[i], interpreters[i], durations[i], cover_urls[i]) for i in range(len(cover_urls))]
        return playlist
       
        

class PageDriver(webdriver.Firefox) :
    def __init__(self) :
        super().__init__(executable_path=PATH_GECKODRIVER)
        self.still_loading = False

    def find_element(self, by=..., value=None) :
        if self.still_loading :
            self.still_loading = False
            return WebDriverWait(self, 10).until(EC.element_to_be_clickable((by, value)))
        return super().find_element(by, value)

    def find_elements(self, by=..., value=None, min_count=0) :
        while self.still_loading :
            elements = super().find_elements(by, value)
            if len(elements) > min_count :
                self.still_loading = False
                return elements
        return super().find_elements(by, value)

    def load_page(self, url) :
        self.get(url)
        self.still_loading = True
    
    def authenticate(self, user, passw) :
        self.load_page(SPOTIFY_LOGIN)
        self.find_element(By.ID, "login-username").send_keys(user)
        self.find_element(By.ID, "login-password").send_keys(passw)
        self.find_element(By.XPATH, LOGIN_BUTTON).click()
        time.sleep(0.2)

    def search(self, tags, url=SPOTIFY_URL, min_count=0) :
        elements = []
        self.load_page(url)
        for name_tag in tags :
            elements.append(self.find_elements(By.CLASS_NAME, name_tag, min_count=min_count))
        return elements


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

    def get_information(self) :
        return self.name, self.interpreter

    def get_duration(self) :
        return self.duration

    def get_cover_url(self) :
        return self.cover_url