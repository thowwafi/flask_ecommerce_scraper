# import json
# import os
# from pprint import pprint
# import requests
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# import sys

# home = os.getcwd()
# CHROMEDRIVER_PATH = os.path.join(home, "chromedriver")
# web_url = "http://tokopedia.com"
# url = "https://gql.tokopedia.com/"

# def check_chrome_driver():
#     try:
#         options = Options()
#         # options.add_argument("--headless")
#         return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
#     except OSError:
#         sys.exit("Chrome webdriver not matching with OS")
#     except Exception as e:
#         sys.exit(str(e))

# if __name__ == "__main__":
#     driver = check_chrome_driver()
#     driver.get(web_url)

import json
import os
import requests
from requests.sessions import session
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.keys import Keys
import sys
import time

SRC = os.getcwd()
HOME = os.path.dirname(SRC)
CHROMEDRIVER_PATH = "./chromedriver"


def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)


def check_driver():
    try:
        options = ChromeOptions()
        # options.add_argument("--headless")
        return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    except OSError:
        sys.exit("Chrome webdriver not matching with OS")
    except Exception as e:
        sys.exit(str(e))

if __name__ == '__main__':
    url = "https://www.tokopedia.com/"
    # headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 OPR/58.0.3135.79'}
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36",
        "authority": "gql.tokopedia.com",
        "method": "POST",
        "path": "/",
        "scheme": "https",
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "cache-control": "no-cache",
        "content-length": "627",
        "content-type": "application/json",
        "origin": "https://www.tokopedia.com",
        "pragma": "no-cache",
        "referer": "https://www.tokopedia.com/",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "x-device": "desktop",
        "x-source": "tokopedia-lite",
        "x-tkpd-lite-service": "zeus",
        "x-version": "f923518",
}
    # session = requests.Session()
    # try:
    #     req = session.get(url, headers=headers)
    # except Exception as e:
    #     print(e)

    # req = requests.get(url, headers=headers)

    # bs = BeautifulSoup(req.text, "html.parser")
    # print(url)
    # response = requests.get(url)
    # import pdb; pdb.set_trace()
    driver = check_driver()
    driver.get(url)
    my_element = driver.find_element_by_xpath("//button[text()='Masuk']")
    my_element.click()
    sleep_time(3)
    element = driver.find_element_by_id("email-phone")
    element.send_keys("087877544953" + Keys.ENTER)
    sleep_time(3)
    # element = driver.find_element_by_id("password-input")
    # element.send_keys("Alpiphysics_27" + Keys.ENTER)
    # sleep_time(3)
    element_ = driver.find_elements_by_xpath("//*[@class='unf-card css-19d2cr0-unf-card e1ukdezh0']")
    if element_:
        print("Got it")
        element_[0].click()
    sleep_time(10)
    print("Input OTP")
    otp = input()
    otp_element = driver.find_elements_by_xpath("//*[@class='css-1ca56s1']")
    if otp_element:
        print("Got it")
        otp_element[0].send_keys(otp + Keys.ENTER)
    sleep_time(5)
    driver.get(url + "order-list")
    print(driver.get_cookies())
    cookies = driver.get_cookies()
    sess = requests.Session()
    for cookie in cookies:
        print(cookie['name'], cookie['value'])
        sess.cookies.set(cookie['name'], cookie['value'])

    payload = [{"operationName":"GetOrderHistory","variables":{"VerticalCategory":"","Status":"","SearchableText":"","CreateTimeStart":"2021-10-13","CreateTimeEnd":"2021-10-14","Page":1,"Limit":10},"query":"query GetOrderHistory($VerticalCategory: String!, $Status: String!, $SearchableText: String!, $CreateTimeStart: String!, $CreateTimeEnd: String!, $Page: Int!, $Limit: Int!) {\n  uohOrders(input: {UUID: \"\", VerticalID: \"\", VerticalCategory: $VerticalCategory, Status: $Status, SearchableText: $SearchableText, CreateTime: \"\", CreateTimeStart: $CreateTimeStart, CreateTimeEnd: $CreateTimeEnd, Page: $Page, Limit: $Limit, SortBy: \"\", IsSortAsc: false}) {\n    orders {\n      orderUUID\n      verticalID\n      verticalCategory\n      userID\n      status\n      verticalStatus\n      searchableText\n      metadata {\n        upstream\n        verticalLogo\n        verticalLabel\n        paymentDate\n        paymentDateStr\n        queryParams\n        listProducts\n        detailURL {\n          webURL\n          webTypeLink\n          __typename\n        }\n        status {\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        products {\n          title\n          imageURL\n          inline1 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          inline2 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          __typename\n        }\n        otherInfo {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        totalPrice {\n          value\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        tickers {\n          action {\n            actionType\n            appURL\n            webURL\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          title\n          text\n          type\n          isFull\n          __typename\n        }\n        buttons {\n          Label\n          variantColor\n          type\n          actionType\n          appURL\n          webURL\n          __typename\n        }\n        dotMenus {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        __typename\n      }\n      createTime\n      createBy\n      updateTime\n      updateBy\n      __typename\n    }\n    totalOrders\n    filtersV2 {\n      label\n      value\n      isPrimary\n      __typename\n    }\n    categories {\n      value\n      label\n      __typename\n    }\n    dateLimit\n    tickers {\n      action {\n        actionType\n        appURL\n        webURL\n        label\n        textColor\n        bgColor\n        __typename\n      }\n      title\n      text\n      type\n      isFull\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)
    gql_url = "https://gql.tokopedia.com/"
    print("here")
    res = sess.post(gql_url, json_data, headers=headers)
    datares = json.loads(res.text)
    print(datares)
    import pdb; pdb.set_trace()
