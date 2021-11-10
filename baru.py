import cfscrape
import os
import requests
from seleniumwire import webdriver
from seleniumwire.undetected_chromedriver import Chrome, ChromeOptions
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
import time
import cloudscraper

def interceptor(request, response):
    print (request.url)

root_path = os.getcwd()
CHROMEDRIVER_PATH = os.path.join(root_path, "chromedriver")

options = ChromeOptions()
#options.add_argument('--headless')
driver = Chrome(options=options, executable_path=CHROMEDRIVER_PATH)
driver.response_interceptor = interceptor
driver.get('https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth')
cookies = driver.get_cookies()
headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9",
    "content-length": "901",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://m.dana.id",
    "referer": "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth",
    "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "macOS",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
}

# scraper = cloudscraper.create_scraper()  # returns a CloudScraper instance
# # Or: scraper = cloudscraper.CloudScraper()  # CloudScraper inherits from requests.Session
# print(scraper.get("https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth").text)
# import pdb; pdb.set_trace()

session = requests.Session()
for cookie in cookies:
    print(cookie['name'], cookie['value'])
    session.cookies.set(cookie['name'], cookie['value'])
scraper = cfscrape.create_scraper(sess=session)
res1 = scraper.get('https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth', headers=headers)
res2 = scraper.get('https://a.m.dana.id/resource/json/ipg/sentry-config.json?params=1636333851460', headers=headers)


import pdb; pdb.set_trace()
time.sleep(3)
