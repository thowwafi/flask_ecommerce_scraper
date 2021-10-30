import ast
import base64
from datetime import datetime
from os import error
from flask import Flask
from flask import request, jsonify
import hashlib
import json
from pprint import pprint
from flask.wrappers import Response
import requests
from selenium.webdriver.common.keys import Keys
import time
from scraper.TokopediaScraper import TokopediaScraper
from utils.utils import sleep_time, makeDirIfNotExists, initialize_webdriver


app = Flask(__name__)
app.config["DEBUG"] = True

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
web_url = "http://tokopedia.com"
url = "https://gql.tokopedia.com/"

@app.route('/')
def hello_world():
    print(app.root_path)
    return "Hello World"


@app.route('/api/request_otp/', methods=['POST'])
def request_otp():
    """
    @Body: 
    {
        "phone": "080989999"
    }
    """
    request_data = request.json
    phone = request_data.get('phone')
    response = {}
    if not phone:
        response['status'] = 'Failed'
        response['message'] = 'Phone cannot be null'
        return jsonify(response), 400

    tokped = TokopediaScraper()
    try:
        data_res = tokped.request_otp(phone)
    except Exception as e:
        response['status'] = 'Failed'
        response['message'] = str(e)
        return jsonify(response), 500

    if isinstance(data_res, list):
        is_success = data_res[0]['data']['OTPRequest']['success']
        if is_success:
            response['status'] = 'Success'
            response['message'] = data_res[0]['data']['OTPRequest']['message']
        else:
            response['status'] = 'Failed'
            response['message'] = data_res[0]['data']['OTPRequest']['errorMessage']
        response['success'] = is_success
    else:
        response = data_res

    return jsonify(response)


@app.route('/api/send_otp/', methods=['POST'])
def send_otp():
    """
    @Body:
    {
        "phone": "080989999",
        "otp": "627091"
    }
    """
    request_data = request.json
    phone = request_data.get('phone')
    otp = request_data.get('otp')

    response = {}
    if not phone or not otp:
        response['status'] = 'Failed'
        response['message'] = 'Phone/OTP cannot be null'
        return jsonify(response), 400

    tokped = TokopediaScraper()
    try:
        data_res, validate_token = tokped.send_otp(phone, otp)
    except Exception as e:
        response['status'] = 'Failed'
        response['message'] = str(e)
        return jsonify(response), 500
    errors = data_res[0]['data']['accountsGetAccountsList']['errors']
    if errors:
        response['status'] = "Failed"
        response['message'] = errors[0]['message']
        return jsonify(response), 500

    response["status"] = "Success"
    response["message"] = ""
    response["validate_token"] = validate_token
    response["user_data"] = data_res[0]['data']['accountsGetAccountsList']
    
    return jsonify(response)


@app.route('/api/login/', methods=['POST'])
def login():
    request_data = request.json
    phone = request_data.get('phone')
    validate_token = request_data.get('validate_token')
    email = request_data.get('email')
    response = {}
    if not phone or not validate_token or not email:
        response['message'] = "phone, validate_token, email cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    tokped = TokopediaScraper()
    login_url = tokped.create_login_url(validate_token, phone)

    try:
        login_data, ok = tokped.login_with_email(driver, email, login_url, phone)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'Failed'
        return jsonify(response), 500
    if not ok:
        response['message'] = str(login_data)
        response['status'] = 'Failed'
        return jsonify(response), 500

    cookies = driver.get_cookies()
    response = {
        "message": "Successfully login",
        "session_token": str(cookies),
        "data": login_data
    }

    return jsonify(response)


@app.route('/api/transaction_list/', methods=['POST'])
def transaction_list():
    request_data = request.json
    session_token = request_data.get('session_token')
    start_at = request_data.get('start_at')
    end_at = request_data.get('end_at')

    response = {}
    if not session_token or not start_at or not end_at:
        response['status'] = 'Failed'
        response['message'] = 'Request body needs session_token, start_at, and end_at value'
        return jsonify(response), 400

    tokped = TokopediaScraper()
    session = tokped.load_session(session_token)
    data = tokped.get_order_history(session, start_at, end_at)

    response['status'] = 'Success.'
    response['message'] = 'Successfully retrieve transactions data.'
    response['data'] = data

    return jsonify(response)


@app.route('/api/get_transactions/', methods=['POST'])
def get_transactions():
    request_data = request.json
    phone = request_data.get('phone')
    start_at = request_data.get('start_at')
    end_at = request_data.get('end_at')
    if not phone or not start_at or not end_at:
        return jsonify({"message": "Phone/Start At/End At cannot be empty."}), 400
    driver, message = initialize_webdriver(app.root_path)
    driver.get(web_url)
    my_element = driver.find_element_by_xpath("//button[text()='Masuk']")
    my_element.click()
    sleep_time(3)
    element = driver.find_element_by_id("email-phone")
    element.send_keys(phone + Keys.ENTER)
    sleep_time(3)
    element_ = driver.find_elements_by_xpath("//*[@class='unf-card css-19d2cr0-unf-card e1ukdezh0']")
    if element_:
        print("Got it")
        element_[0].click()
    sleep_time(5)
    print("Input OTP")
    otp = input()
    otp_element = driver.find_elements_by_xpath("//*[@class='css-1ca56s1']")
    if otp_element:
        print("Got it")
        otp_element[0].send_keys(otp)
    sleep_time(3)
    account_elements = driver.find_elements_by_xpath("//*[@class='css-rcj2s']")
    if account_elements:
        print("Got it")
        account_elements[1].click()
    sleep_time(3)
    personal_pin = driver.find_elements_by_xpath("//*[@class='css-1bzs0jc']")
    if personal_pin:
        print("Input PIN")
        pin_number = input()
        personal_pin[0].send_keys(pin_number)
    sleep_time(5)
    driver.get(web_url + "/order-list")
    print(driver.get_cookies())
    cookies = driver.get_cookies()
    sess = requests.Session()
    for cookie in cookies:
        print(cookie['name'], cookie['value'])
        sess.cookies.set(cookie['name'], cookie['value'])

    payload = [{"operationName":"GetOrderHistory","variables":{"VerticalCategory":"","Status":"","SearchableText":"","CreateTimeStart":start_at,"CreateTimeEnd":end_at,"Page":1,"Limit":10},"query":"query GetOrderHistory($VerticalCategory: String!, $Status: String!, $SearchableText: String!, $CreateTimeStart: String!, $CreateTimeEnd: String!, $Page: Int!, $Limit: Int!) {\n  uohOrders(input: {UUID: \"\", VerticalID: \"\", VerticalCategory: $VerticalCategory, Status: $Status, SearchableText: $SearchableText, CreateTime: \"\", CreateTimeStart: $CreateTimeStart, CreateTimeEnd: $CreateTimeEnd, Page: $Page, Limit: $Limit, SortBy: \"\", IsSortAsc: false}) {\n    orders {\n      orderUUID\n      verticalID\n      verticalCategory\n      userID\n      status\n      verticalStatus\n      searchableText\n      metadata {\n        upstream\n        verticalLogo\n        verticalLabel\n        paymentDate\n        paymentDateStr\n        queryParams\n        listProducts\n        detailURL {\n          webURL\n          webTypeLink\n          __typename\n        }\n        status {\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        products {\n          title\n          imageURL\n          inline1 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          inline2 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          __typename\n        }\n        otherInfo {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        totalPrice {\n          value\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        tickers {\n          action {\n            actionType\n            appURL\n            webURL\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          title\n          text\n          type\n          isFull\n          __typename\n        }\n        buttons {\n          Label\n          variantColor\n          type\n          actionType\n          appURL\n          webURL\n          __typename\n        }\n        dotMenus {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        __typename\n      }\n      createTime\n      createBy\n      updateTime\n      updateBy\n      __typename\n    }\n    totalOrders\n    filtersV2 {\n      label\n      value\n      isPrimary\n      __typename\n    }\n    categories {\n      value\n      label\n      __typename\n    }\n    dateLimit\n    tickers {\n      action {\n        actionType\n        appURL\n        webURL\n        label\n        textColor\n        bgColor\n        __typename\n      }\n      title\n      text\n      type\n      isFull\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)
    gql_url = "https://gql.tokopedia.com/"
    print("here")
    res = sess.post(gql_url, json_data, headers=headers)
    datares = json.loads(res.text)
    print(datares)
    return jsonify(datares)
    

if __name__ == '__main__':
   app.run()
