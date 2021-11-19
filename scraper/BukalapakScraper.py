import ast
import cloudscraper
from datetime import datetime, timedelta
import json
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from utils.utils import sleep_time


class BukalapakScraper:
    login_url = "https://accounts.bukalapak.com/login"

    def request_otp(self, driver, phone):
        driver.get(self.login_url)
        sleep_time(2)
        elem = driver.find_element_by_id("LoginID")
        elem.send_keys(phone)
        elem.send_keys(Keys.ENTER)
        sleep_time(2)
        return driver.get_cookies()

    def send_otp(self, driver, otp, session_token, phone):
        driver.get(self.login_url)
        cookies = ast.literal_eval(session_token)
        for cookie in cookies:
            driver.add_cookie(cookie)
        sleep_time(2)
        elem = driver.find_element_by_id("LoginID")
        elem.send_keys(phone)
        elem.send_keys(Keys.ENTER)
        sleep_time(2)
        import pdb; pdb.set_trace()