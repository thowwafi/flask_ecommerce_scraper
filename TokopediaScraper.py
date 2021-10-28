import base64
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time


def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)

class TokopediaScraper:
    def __init__(self, phone=""):
        self.phone = phone
        self.encoded_phone = self.encode_phone()
        self.url = self.get_url()

    def encode_phone(self):
        """
        Encode phone number with base64
        """
        encoded = base64.b64encode(self.phone.encode('utf-8'))
        return encoded.decode()  # turn bytes to string

    def get_url(self):
        """
        Generate url from encoded phone number
        """
        return f"https://accounts.tokopedia.com/otp/c/page?otp_type=112&m_encd={self.encoded_phone}&popup=false&header=true&redirect_parent=false&ld=https%3A%2F%2Faccounts.tokopedia.com%2Flpn%2Fusers%3Fencoded%3D{self.encoded_phone}%26client_id%3D%26redirect_uri%3D%26state%3D"

    def request_otp(self, driver):
        """
        Send GET request to URL to get OTP
        """
        driver.get(self.url)
        sleep_time(2)
        driver.find_element_by_id("cotp__method--sms").click()
        sleep_time(1)
        driver.quit()