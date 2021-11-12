import ast
from bs4 import BeautifulSoup
import json
import re
import requests
from requests.api import head
from selenium.webdriver.common.keys import Keys
from utils.utils import sleep_time
import cloudscraper


class DanaScraper:
    base_url = "https://m.dana.id/d/portal/oauth"
    login_url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    pocket_url = "https://m.dana.id/d/pocket"
    completed_url = "https://m.dana.id/i/transaction/list/completed"
    otp_url = "https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-81272709003&riskPhoneNumber=62-812%2a%2a%2a%2a9003&verificationMethods=OTP_SMS&securityId=sidfe6627c617ec6f05c25cfcb4ae203011_crc&credentials=UGm4L4XrJizkp3slNgbV8CcrZ2YAhQneigN0R2rp5lrjXCFX1uiDiTndH9gFtuMcuXsq4ue69eCbaQGNbbPPkaecAiI29u2MnZs9PgxV9kDrHznT6ZgHGcoLQY5bNydYYbXWfwK6%2BtJ0wqB4R5jROxJy73%2FltF1T4oiwKJASmLNTecAd7guZgY8t%2Bdjcg8K3WDJdS3HB91BpJIykKCXEMEUBObTw5kEfEF%2BTrvNjAitFV3h3U1v7n3imp8C9etm%2BV%2B2TVbzAJlfMjR9n1VAk%2Beyjrwpd%2BTWqhJ2kg62VC%2BHn%2BzoWbvpP1H75G4KbSg91G2dmaMxJhbKEqJscoiVOIw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth"

    def request_otp(self, driver, phone, pin):
        driver.get(self.login_url)
        elem = driver.find_element_by_xpath("//input")
        elem.send_keys(phone + Keys.ENTER)
        sleep_time(2)
        for p in pin:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(p)
        sleep_time(2)
        return driver.current_url.split("securityId=")[1]

    def split_session_token(self, session_token):
        session_token_plus = ast.literal_eval(session_token)
        session_token = [token for token in session_token_plus if token.get('name') != 'security_id']
        security_id = [token for token in session_token_plus if token.get('name') == 'security_id']
        value = security_id[0].get('value')
        return session_token, value

    def get_login_url(self, phone, security_id):
        return f"https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-{phone}&riskPhoneNumber=62-{phone[:3]}%2a%2a%2a%2a{phone[-4:]}&verificationMethods=OTP_SMS&securityId={security_id}"

    def create_cookie_list(self, cookies):
        cookie_list = []
        splitted = cookies.split(";")
        for cookie in splitted:
            cookie = cookie.strip()
            if not cookie:
                continue
            name, value =  cookie.split('=', 1)
            cookie_list.append({"name": name, "value": value})
        return cookie_list

    def send_otp(self, driver, security_id, otp, cookies, phone):
        driver.get(self.login_url)

        for cookie in cookies:
            driver.add_cookie(cookie)

        url = self.get_login_url(phone, security_id)
        print(url)
        driver.get(url)
        sleep_time(3)
        for o in otp:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(o)
        sleep_time(3)
        driver.get(self.pocket_url)
        driver.get(self.completed_url)
        sleep_time(3)

        return "".join(
            f"{cookie['name']}={cookie['value']};"
            for cookie in driver.get_cookies()
            if cookie['name'] in ['ALIPAYJSESSIONID', '__cf_bm']
        )

    def get_transactions(self, login_cookie):
        headers = {
            "Host": "m.dana.id",
            "x-fe-version": "1.97.0",
            "referrer": "https://m.dana.id/i/transaction/list/progressing",
            "x-appkey": "23936057",
            "user-agent": "Skywalker/2.0.0 EDIK/1.0.0 Dalvik/2.1.0 (Linux; Android 5.1; PRO 5 Build/LMY47D)",
            "cookie": login_cookie,
            "content-type": "application/json; charset\u003dutf-8",
        }
        payload = {
            "transactionQueryType": "COMPLETED", "pageNum":1
        }
        url = "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.transaction.list.json"
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

        res = scraper.post(url, headers=headers, data=json.dumps(payload))

        return res.json()
