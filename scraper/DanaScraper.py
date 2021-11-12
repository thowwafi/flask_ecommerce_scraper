import cloudscraper
from datetime import datetime, timedelta
import json
from selenium.webdriver.common.keys import Keys
from utils.utils import sleep_time


class DanaScraper:
    base_url = "https://m.dana.id/d/portal/oauth"
    login_url = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    pocket_url = "https://m.dana.id/d/pocket"
    completed_url = "https://m.dana.id/i/transaction/list/completed"
    otp_url = "https://m.dana.id/d/ipg/loginrisk?phoneNumber=62-81272709003&riskPhoneNumber=62-812%2a%2a%2a%2a9003&verificationMethods=OTP_SMS&securityId=sidfe6627c617ec6f05c25cfcb4ae203011_crc&credentials=UGm4L4XrJizkp3slNgbV8CcrZ2YAhQneigN0R2rp5lrjXCFX1uiDiTndH9gFtuMcuXsq4ue69eCbaQGNbbPPkaecAiI29u2MnZs9PgxV9kDrHznT6ZgHGcoLQY5bNydYYbXWfwK6%2BtJ0wqB4R5jROxJy73%2FltF1T4oiwKJASmLNTecAd7guZgY8t%2Bdjcg8K3WDJdS3HB91BpJIykKCXEMEUBObTw5kEfEF%2BTrvNjAitFV3h3U1v7n3imp8C9etm%2BV%2B2TVbzAJlfMjR9n1VAk%2Beyjrwpd%2BTWqhJ2kg62VC%2BHn%2BzoWbvpP1H75G4KbSg91G2dmaMxJhbKEqJscoiVOIw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    headers = {}

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
        tokens, security_id = session_token.split(";security_id=")
        cookies = [{
            "name": tokens.split("=")[0],
            "value": tokens.split("=")[1],
            'path': '/',
            'domain': '.m.dana.id',
            'secure': True,
            'httpOnly': True,
            'sameSite': 'Lax'
        }]
        return cookies, security_id

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
        sleep_time(2)
        for o in otp:
            elem = driver.find_element_by_xpath("//input")
            elem.send_keys(o)
        sleep_time(2)
        driver.get(self.pocket_url)
        driver.get(self.completed_url)
        sleep_time(2)

        return "".join(
            f"{cookie['name']}={cookie['value']};"
            for cookie in driver.get_cookies()
            if cookie['name'] in ['ALIPAYJSESSIONID', '__cf_bm']
        )

    def convert_date(self, start_at, end_at):
        start_at = datetime.strptime(start_at, "%Y-%m-%d")
        start_at_time = int(start_at.timestamp() * 1000)
        end_at = datetime.strptime(end_at, "%Y-%m-%d")
        end_at = end_at + timedelta(days=1)
        end_at_time = int((end_at.timestamp() * 1000) - 1)
        return start_at_time, end_at_time

    def get_transactions(self, login_cookie, start_date, end_date):
        self.headers['cookie'] = login_cookie
        payload = {
            "transactionQueryType": "COMPLETED", "pageNum":1,
            "startDate": start_date,
            "endDate": end_date
        }
        print(payload)
        url = "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.transaction.list.json"
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})

        return scraper.post(url, headers=self.headers, data=json.dumps(payload))

    def get_user_info(self, login_cookie):
        self.headers['cookie'] = login_cookie
        url = "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.information.more.json"
        payload = {"queryType":"FULL"}
        scraper = cloudscraper.create_scraper(browser={'browser': 'firefox','platform': 'windows','mobile': False})
        return scraper.post(url, headers=self.headers, data=json.dumps(payload))
