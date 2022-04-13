from selenium import webdriver
from selenium.webdriver.common.by import By

from settings import *


class PageDriver :
    def __init__(self) :
        self.browser = webdriver.Firefox(executable_path=PATH_GECKODRIVER)
        self.browser.get(SPOTIFY_URL)

    def authenticate(self, user, passw) :
        user_input = self.browser.find_element(By.ID, "login-username")
        passw_input = self.browser.find_element(By.ID, "login-password")

        user_input.send_keys(user)
        passw_input.send_keys(passw)

        self.browser.find_element(By.XPATH, LOGIN_BUTTON).click()


class SpotifyFront :
    def __init__(self, user, passw) :
        driver = PageDriver()
        driver.authenticate(user, passw)