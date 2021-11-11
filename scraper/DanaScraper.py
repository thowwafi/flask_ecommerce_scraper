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
        return session_token.split("_____security_id=")

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
        cookie_list = self.create_cookie_list(cookies)
        for cookie in cookie_list:
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

        login_cookie = "".join(
            f"{cookie['name']}={cookie['value']}; "
            for cookie in driver.get_cookies()
        )

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
        import pdb; pdb.set_trace()
        # orders_card = driver.find_elements_by_xpath("//div[@class='order-wrapper-card']")
        # orders_count = len(orders_card)
        # data = []
        # for i in range(orders_count):
        #     order = {}
        #     ord_elem = driver.find_elements_by_xpath("//div[@class='order-wrapper-card']")[i]
        #     amount_text = ord_elem.find_element_by_xpath("//span[@class='card-amount order-amount']").text.strip()
        #     order['amount'] = amount_text
        #     ord_elem.click()
        #     sleep_time(1)
        #     # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
        #     driver.add_cdp_listener('Network.getResponseBody', mylousyprintfunction)

        #     if driver.find_elements_by_xpath("//div[@class='wrapper-transaction-detail']"):
        #         soup = BeautifulSoup(driver.page_source, 'html.parser')
        #         order['order_title'] = soup.find("p", {"class": "header-desc"}).text.strip()
        #         order['payment_method'] = soup.find("div", {"class": "transaction-change-bank"}).text.strip()
        #         order['amount'] = soup.find("p", {"class": "header-amount"}).text.strip()
        #         summaries = soup.find_all("div", {"class": "summary-info"})
        #         for summary in summaries:
        #             order[summary.find_all("div")[0].text.strip()] = summary.find_all("div")[1].text.strip()
        #         sleep_time(1)
        #     driver.get(self.completed_url)
        #     sleep_time(1)
        #     data.append(order)

        return res.json()
