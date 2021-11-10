import ast
from bs4 import BeautifulSoup
import json
import re
import requests
from selenium.webdriver.common.keys import Keys
from utils.utils import sleep_time


class DanaScraper:
    base_url = "https://m.dana.id/d/portal/oauth"
    login_url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    pocket_url = "https://m.dana.id/d/pocket"
    completed_url = "https://m.dana.id/d/ipg/completed"
    otp_url = "https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-81272709003&riskPhoneNumber=62-812%2a%2a%2a%2a9003&verificationMethods=OTP_SMS&securityId=sidfe6627c617ec6f05c25cfcb4ae203011_crc&credentials=UGm4L4XrJizkp3slNgbV8CcrZ2YAhQneigN0R2rp5lrjXCFX1uiDiTndH9gFtuMcuXsq4ue69eCbaQGNbbPPkaecAiI29u2MnZs9PgxV9kDrHznT6ZgHGcoLQY5bNydYYbXWfwK6%2BtJ0wqB4R5jROxJy73%2FltF1T4oiwKJASmLNTecAd7guZgY8t%2Bdjcg8K3WDJdS3HB91BpJIykKCXEMEUBObTw5kEfEF%2BTrvNjAitFV3h3U1v7n3imp8C9etm%2BV%2B2TVbzAJlfMjR9n1VAk%2Beyjrwpd%2BTWqhJ2kg62VC%2BHn%2BzoWbvpP1H75G4KbSg91G2dmaMxJhbKEqJscoiVOIw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    headers = {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "cache-control": "no-cache",
        "content-length": "135",
        "content-type": "application/json",
        "origin": "https://m.dana.id",
        "pragma": "no-cache",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    def login(self, driver, phone, pin):
        # res = requests.get(self.login_url)
        driver.get(self.login_url)
        elem = driver.find_element_by_xpath("//input")
        elem.send_keys(phone + Keys.ENTER)
        sleep_time(5)
        for p in pin:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(p)
        sleep_time(5)
        return driver.current_url.split("securityId=")[1]

        # print("Input OTP")
        # otp = input()
        # for p in otp:
        #     elem = driver.find_element_by_xpath("//input")
        #     elem.send_keys(p)
        # sleep_time(2)
        # driver.get(self.pocket_url)
        # driver.get(self.completed_url)
        # import pdb; pdb.set_trace()

    def send_otp(self, driver, security_id, otp, cookies, phone):
        import undetected_chromedriver.v2 as uc
        from pprint import pformat
        def mylousyprintfunction(eventdata):
            print(eventdata)
            # if eventdata['params']['response']['url'] == "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.transaction.list.json":

        driver = uc.Chrome(enable_cdp_events=True)
        driver.get(self.login_url)
        cookies = ast.literal_eval(cookies)
        for cookie in cookies:
            cookie['sameSite'] = "Lax"
            driver.add_cookie(cookie)
        url = f"https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-{phone}&riskPhoneNumber=62-{phone[:3]}%2a%2a%2a%2a{phone[-4:]}&verificationMethods=OTP_SMS&securityId={security_id}"
        print(url)
        driver.get(url)
        sleep_time(5)
        for o in otp:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(o)
        sleep_time(5)
        driver.get(self.pocket_url)
        driver.get(self.completed_url)
        sleep_time(5)
        orders_card = driver.find_elements_by_xpath("//div[@class='order-wrapper-card']")
        orders_count = len(orders_card)
        data = []
        for i in range(orders_count):
            order = {}
            ord_elem = driver.find_elements_by_xpath("//div[@class='order-wrapper-card']")[i]
            amount_text = ord_elem.find_element_by_xpath("//span[@class='card-amount order-amount']").text.strip()
            order['amount'] = amount_text
            ord_elem.click()
            sleep_time(1)
            # driver.add_cdp_listener('Network.responseReceived', mylousyprintfunction)
            driver.add_cdp_listener('Network.getResponseBody', mylousyprintfunction)

            if driver.find_elements_by_xpath("//div[@class='wrapper-transaction-detail']"):
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                order['order_title'] = soup.find("p", {"class": "header-desc"}).text.strip()
                order['payment_method'] = soup.find("div", {"class": "transaction-change-bank"}).text.strip()
                order['amount'] = soup.find("p", {"class": "header-amount"}).text.strip()
                summaries = soup.find_all("div", {"class": "summary-info"})
                for summary in summaries:
                    order[summary.find_all("div")[0].text.strip()] = summary.find_all("div")[1].text.strip()
                sleep_time(1)
            driver.get(self.completed_url)
            sleep_time(1)
            data.append(order)

        return data
