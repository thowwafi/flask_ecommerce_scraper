import ast
import pickle
import requests
from selenium.webdriver.common.keys import Keys
from utils.utils import sleep_time


class DanaScraper:
    # login_url = "https://m.dana.id/d/portal/oauth"
    login_url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    pocket_url = "https://m.dana.id/d/pocket"
    completed_url = "https://m.dana.id/d/ipg/completed"
    otp_url = "https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-81272709003&riskPhoneNumber=62-812%2a%2a%2a%2a9003&verificationMethods=OTP_SMS&securityId=sidfe6627c617ec6f05c25cfcb4ae203011_crc&credentials=UGm4L4XrJizkp3slNgbV8CcrZ2YAhQneigN0R2rp5lrjXCFX1uiDiTndH9gFtuMcuXsq4ue69eCbaQGNbbPPkaecAiI29u2MnZs9PgxV9kDrHznT6ZgHGcoLQY5bNydYYbXWfwK6%2BtJ0wqB4R5jROxJy73%2FltF1T4oiwKJASmLNTecAd7guZgY8t%2Bdjcg8K3WDJdS3HB91BpJIykKCXEMEUBObTw5kEfEF%2BTrvNjAitFV3h3U1v7n3imp8C9etm%2BV%2B2TVbzAJlfMjR9n1VAk%2Beyjrwpd%2BTWqhJ2kg62VC%2BHn%2BzoWbvpP1H75G4KbSg91G2dmaMxJhbKEqJscoiVOIw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth"

    def login(self, driver, phone, pin):
        # res = requests.get(self.login_url)
        driver.get(self.login_url)
        elem = driver.find_element_by_xpath("//input")
        elem.send_keys(phone + Keys.ENTER)
        sleep_time(2)
        for p in pin:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(p)
        sleep_time(2)
        return driver.current_url

        # print("Input OTP")
        # otp = input()
        # for p in otp:
        #     elem = driver.find_element_by_xpath("//input")
        #     elem.send_keys(p)
        # sleep_time(2)
        # driver.get(self.pocket_url)
        # driver.get(self.completed_url)
        # import pdb; pdb.set_trace()

    def send_otp(self, driver, url, otp, cookies):
        driver.get(self.login_url)

        cookies = ast.literal_eval(cookies)
        for cookie in cookies:
            driver.add_cookie(cookie)
        
        driver.get(url)
        sleep_time(2)
        for o in otp:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(o)
        sleep_time(2)
        driver.get(self.pocket_url)
        driver.get(self.completed_url)

        # https://m.dana.id/d/portal/transaction?bizOrderId=2021091210121481030100166508924906902&paymentOrderId=2021091210110000010000DANAW3ID166508914488553
        import pdb; pdb.set_trace()


