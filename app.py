import ast
import base64
from datetime import datetime
from flask import Flask
from flask import request, jsonify
from flask import Response
import hashlib
import json
import os
from pprint import pprint
import pickle
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from seleniumrequests import Chrome
import sys
import time
from .TokopediaScraper import TokopediaScraper


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
headers2 = {
    "authority": "gql.tokopedia.com",
    "method": "POST",
    "path": "/",
    "scheme": "https",
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.9,id;q=0.8",
    "cache-control": "no-cache",
    "content-length": "656",
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
    "x-tkpd-akamai": "otp",
    "x-tkpd-lite-service": "zeus",
    "x-version": "f923518"
}
web_url = "http://tokopedia.com"
url = "https://gql.tokopedia.com/"

@app.route('/')
def hello_world():
    print(app.root_path)
    return "Hello World"

def initialize_webdriver():
    CHROMEDRIVER_PATH = os.path.join(app.root_path, "chromedriver")
    try:
        options = Options()
        # options.add_argument("--headless")
        return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options), "Ok"
    except OSError:
        return None, "Chrome webdriver not matching with OS"
    except Exception as e:
        return None, e

def create_response(message, status):
    return jsonify({
        "message": message,
        "status": status
    })


@app.route('/api/login/', methods=['POST'])
def login():
    request_data = request.json
    if not request_data:
        return jsonify({"message": "Phone cannot be blank."}), 400

    if "phone" not in request_data:
        return jsonify({"message": "Phone cannot be blank."}), 400

    phone = request_data.get('phone')
    if phone is None:
        return jsonify({"message": "Phone cannot be null."}), 400
    phone = phone.strip()
    if not phone:
        return jsonify({"message": "Phone cannot be null."}), 400

    payload = [
        {
            "operationName":"OTPRequest","variables":{"msisdn":phone,"otpType":"112","mode":"sms","otpDigit":6},
            "query":"query OTPRequest($otpType: String!, $mode: String, $msisdn: String, $email: String, $otpDigit: Int, $ValidateToken: String, $UserIDEnc: String) {\n  OTPRequest(otpType: $otpType, mode: $mode, msisdn: $msisdn, email: $email, otpDigit: $otpDigit, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {\n    success\n    message\n    errorMessage\n    sse_session_id\n    list_device_receiver\n    error_code\n    message_title\n    message_sub_title\n    message_img_link\n    __typename\n  }\n}\n"
        }
    ]
    json_data = json.dumps(payload)

    sess = requests.Session()
    res = sess.get(web_url, headers=headers)
    cookies_ = sess.cookies.get_dict()
    for key, value in cookies_.items():
        sess.cookies.set(key, value)
    pprint(headers)
    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)
    print("datares", datares)
    response = {}
    if isinstance(datares, list):
        response['message'] = datares[0]['data']['OTPRequest']['message']
        response['errorMessage'] = datares[0]['data']['OTPRequest']['errorMessage']
        response['success'] = datares[0]['data']['OTPRequest']['success']
        response['cookies'] = str(cookies_new)
    else:
        response = datares
    print(response)
    return jsonify(response)


@app.route('/api/send_otp/', methods=['POST'])
def send_otp():
    request_data = request.json

    if "phone" not in request_data:
        return jsonify({"message": "Phone cannot be blank."}), 400
    if "otp" not in request_data:
        return jsonify({"message": "OTP cannot be blank."}), 400
    if "cookies" not in request_data:
        return jsonify({"message": "Cookies cannot be blank."}), 400

    phone = request_data.get('phone')
    if phone is None:
        return jsonify({"message": "Phone cannot be null."}), 400
    phone = phone.strip()
    if not phone:
        return jsonify({"message": "Phone cannot be null."}), 400

    otp = request_data.get('otp')
    cookies = request_data.get('cookies')
    if not cookies:
        return jsonify({"message": "Cookies not found."}), 400
    if not otp:
        return jsonify({"message": "OTP not found."}), 400

    payload = [{"operationName":"OTPValidate","variables":{"msisdn":phone,"code":otp,"otpType":"112","mode":"sms"},"query":"query OTPValidate($msisdn: String, $code: String!, $otpType: String, $fpData: String, $getSL: String, $email: String, $mode: String, $ValidateToken: String, $UserIDEnc: String) {\n  OTPValidate(code: $code, otpType: $otpType, msisdn: $msisdn, fpData: $fpData, getSL: $getSL, email: $email, mode: $mode, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {\n    success\n    message\n    errorMessage\n    validateToken\n    cookieList {\n      key\n      value\n      expire\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)

    sess = requests.Session()
    cookies_dict = ast.literal_eval(cookies)
    for key, value in cookies_dict.items():
        sess.cookies.set(key, value)

    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)
    print("datares", datares)

    # payload = [{"operationName":"isAuthenticatedQuery","variables":{},"query":"query isAuthenticatedQuery {\n  isAuthenticated\n}\n"}]
    # json_data = json.dumps(payload)
    # res = sess.post(url, json_data, headers=headers)
    
    datares[0]['cookies'] = str(cookies_new)
    return jsonify(datares)


@app.route('/api/account_list/', methods=['POST'])
def account_list():
    request_data = request.json
    phone = request_data.get('phone')
    validate_token = request_data.get('validate_token')
    cookies = request_data.get('cookies')

    payload = [{"operationName":"AccountListQuery","variables":{"validate_token":validate_token,"phone":phone,"login_type":""},"query":"query AccountListQuery($validate_token: String!, $phone: String!, $login_type: String) {\n  accountsGetAccountsList(validate_token: $validate_token, phone: $phone, login_type: $login_type) {\n    key\n    msisdn_view\n    msisdn\n    users_details {\n      user_id\n      fullname\n      email\n      msisdn_verified\n      image\n      shop_detail {\n        id\n        name\n        domain\n        __typename\n      }\n      challenge_2fa\n      user_id_enc\n      __typename\n    }\n    users_count\n    errors {\n      name\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)

    sess = requests.Session()
    cookies_dict = ast.literal_eval(cookies)
    for key, value in cookies_dict.items():
        sess.cookies.set(key, value)

    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)

    datares[0]['cookies'] = str(cookies_new)
    return jsonify(datares)


@app.route('/api/login_mutation/', methods=['POST'])
def login_mutation():
    request_data = request.json
    phone = request_data.get('phone')
    username = request_data.get('username')
    password = request_data.get('password')
    cookies = request_data.get('cookies')

    string = base64.b64encode(password.encode('utf-8'))
    pas_md5 = hashlib.md5(string).hexdigest() + "=Xg5k"

    encoded = base64.b64encode(username.encode('utf-8'))
    username_enc = encoded.decode() + "Xg5k"

    payload = [{"operationName":"LoginMutation","variables":{"input":{"grant_type":"cGFzc3dvcmQ=Xg5k","password_type":"lpn","code":phone,"username":username_enc,"password":pas_md5,"supported":"true"}},"query":"mutation LoginMutation($input: TokenRequest!) {\n  login_token(input: $input) {\n    access_token\n    refresh_token\n    token_type\n    sid\n    acc_sid\n    errors {\n      message\n      __typename\n    }\n    popup_error {\n      header\n      body\n      action\n      __typename\n    }\n    sq_check\n    cotp_url\n    uid\n    action\n    event_code\n    expires_in\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)

    cookies_dict = ast.literal_eval(cookies)

    sess = requests.Session()
    for key, value in cookies_dict.items():
        sess.cookies.set(key, value)

    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)

    datares[0]['cookies'] = str(cookies_new)
    return jsonify(datares)


def sleep_time(number):
    for i in range(number, 0, -1):
        print(f"{i}", end='\n', flush=True)
        time.sleep(1)


@app.route('/api/request_otp/', methods=['POST'])
def request_otp():
    request_data = request.json
    phone = request_data.get('phone')

    tokped = TokopediaScraper(phone=phone)

    response = {}
    driver, message = initialize_webdriver()
    if not driver:
        response['message'] = message
        response['status'] = 'Failed'
        return jsonify(response)

    try:
        tokped.request_otp(driver)
    except Exception as e:
        response['message'] = e
        response['status'] = 'Failed'
        return jsonify(response)

    response['message'] = "SMS has been sent."
    response['status'] = "Success"
    response['otp_token'] = tokped.encoded_phone
    return jsonify(response)


@app.route('/api/send_otp/', methods=['POST'])
def send_otp():
    request_data = request.json
    otp = request_data.get('otp')
    otp_token = request_data.get('otp_token')
    email = request_data.get('email')

    
    driver, message = initialize_webdriver()
    driver.get(url)
    sleep_time(3)
    driver.find_element_by_id("cotp__method--sms").click()
    sleep_time(3)
    for index, number in enumerate(otp, start=1):
        driver.find_element_by_id(f"otp-number-input-{index}").send_keys(number)
    sleep_time(3)
    email_choices = driver.find_elements_by_xpath("//p[@class='m-0']")
    if email_choices and email:
        selected_el = [e for e in email_choices if e.text == email]
        selected_el[0].click()
    driver.get(web_url + "/order-list")
    sleep_time(3)
    session_id = datetime.now().strftime("%Y%m%d%H%M%S")
    cookies_folder = os.path.join(app.instance_path, 'cookies')
    if not os.path.exists(cookies_folder):
        os.makedirs(cookies_folder)
    cookie_file = os.path.join(cookies_folder, f"cookies_{session_id}.pkl")
    pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
    response = {
        "message": "Successfully login",
        "session_id": session_id
    }
    driver.quit()
    return jsonify(response)


@app.route('/api/new_transactions/', methods=['POST'])
def new_transactions():
    cookies = pickle.load(open("cookies.pkl", "rb"))
    sess = requests.Session()
    for cookie in cookies:
        print(cookie['name'], cookie['value'])
        sess.cookies.set(cookie['name'], cookie['value'])

    payload = [{"operationName":"GetOrderHistory","variables":{"VerticalCategory":"","Status":"","SearchableText":"","CreateTimeStart":"2021-10-01","CreateTimeEnd":"2021-10-11","Page":1,"Limit":10},"query":"query GetOrderHistory($VerticalCategory: String!, $Status: String!, $SearchableText: String!, $CreateTimeStart: String!, $CreateTimeEnd: String!, $Page: Int!, $Limit: Int!) {\n  uohOrders(input: {UUID: \"\", VerticalID: \"\", VerticalCategory: $VerticalCategory, Status: $Status, SearchableText: $SearchableText, CreateTime: \"\", CreateTimeStart: $CreateTimeStart, CreateTimeEnd: $CreateTimeEnd, Page: $Page, Limit: $Limit, SortBy: \"\", IsSortAsc: false}) {\n    orders {\n      orderUUID\n      verticalID\n      verticalCategory\n      userID\n      status\n      verticalStatus\n      searchableText\n      metadata {\n        upstream\n        verticalLogo\n        verticalLabel\n        paymentDate\n        paymentDateStr\n        queryParams\n        listProducts\n        detailURL {\n          webURL\n          webTypeLink\n          __typename\n        }\n        status {\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        products {\n          title\n          imageURL\n          inline1 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          inline2 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          __typename\n        }\n        otherInfo {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        totalPrice {\n          value\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        tickers {\n          action {\n            actionType\n            appURL\n            webURL\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          title\n          text\n          type\n          isFull\n          __typename\n        }\n        buttons {\n          Label\n          variantColor\n          type\n          actionType\n          appURL\n          webURL\n          __typename\n        }\n        dotMenus {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        __typename\n      }\n      createTime\n      createBy\n      updateTime\n      updateBy\n      __typename\n    }\n    totalOrders\n    filtersV2 {\n      label\n      value\n      isPrimary\n      __typename\n    }\n    categories {\n      value\n      label\n      __typename\n    }\n    dateLimit\n    tickers {\n      action {\n        actionType\n        appURL\n        webURL\n        label\n        textColor\n        bgColor\n        __typename\n      }\n      title\n      text\n      type\n      isFull\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)
    gql_url = "https://gql.tokopedia.com/"
    res = sess.post(gql_url, json_data, headers=headers)
    datares = json.loads(res.text)
    return jsonify(datares)


@app.route('/api/get_transactions/', methods=['POST'])
def get_transactions():
    request_data = request.json
    phone = request_data.get('phone')
    start_at = request_data.get('start_at')
    end_at = request_data.get('end_at')
    if not phone or not start_at or not end_at:
        return jsonify({"message": "Phone/Start At/End At cannot be empty."}), 400
    driver, message = initialize_webdriver()
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
    

@app.route('/api/transactions/', methods=['GET', 'POST'])
def transactions():
    # payload = [{"operationName":"GetOrderHistory","variables":{"VerticalCategory":"","Status":"","SearchableText":"","CreateTimeStart":"2021-10-13","CreateTimeEnd":"2021-10-14","Page":1,"Limit":10},"query":"query GetOrderHistory($VerticalCategory: String!, $Status: String!, $SearchableText: String!, $CreateTimeStart: String!, $CreateTimeEnd: String!, $Page: Int!, $Limit: Int!) {\n  uohOrders(input: {UUID: \"\", VerticalID: \"\", VerticalCategory: $VerticalCategory, Status: $Status, SearchableText: $SearchableText, CreateTime: \"\", CreateTimeStart: $CreateTimeStart, CreateTimeEnd: $CreateTimeEnd, Page: $Page, Limit: $Limit, SortBy: \"\", IsSortAsc: false}) {\n    orders {\n      orderUUID\n      verticalID\n      verticalCategory\n      userID\n      status\n      verticalStatus\n      searchableText\n      metadata {\n        upstream\n        verticalLogo\n        verticalLabel\n        paymentDate\n        paymentDateStr\n        queryParams\n        listProducts\n        detailURL {\n          webURL\n          webTypeLink\n          __typename\n        }\n        status {\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        products {\n          title\n          imageURL\n          inline1 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          inline2 {\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          __typename\n        }\n        otherInfo {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        totalPrice {\n          value\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        tickers {\n          action {\n            actionType\n            appURL\n            webURL\n            label\n            textColor\n            bgColor\n            __typename\n          }\n          title\n          text\n          type\n          isFull\n          __typename\n        }\n        buttons {\n          Label\n          variantColor\n          type\n          actionType\n          appURL\n          webURL\n          __typename\n        }\n        dotMenus {\n          actionType\n          appURL\n          webURL\n          label\n          textColor\n          bgColor\n          __typename\n        }\n        __typename\n      }\n      createTime\n      createBy\n      updateTime\n      updateBy\n      __typename\n    }\n    totalOrders\n    filtersV2 {\n      label\n      value\n      isPrimary\n      __typename\n    }\n    categories {\n      value\n      label\n      __typename\n    }\n    dateLimit\n    tickers {\n      action {\n        actionType\n        appURL\n        webURL\n        label\n        textColor\n        bgColor\n        __typename\n      }\n      title\n      text\n      type\n      isFull\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    payload = [{"operationName":"isAuthenticatedQuery","variables":{},"query":"query isAuthenticatedQuery {\n  isAuthenticated\n}\n"}]
    json_data = json.dumps(payload)
    request_data = request.json
    cookies = request_data.get('cookies')
    sess = requests.Session()
    for key, value in cookies.items():
        sess.cookies.set(key, value)
    res_ = sess.get(web_url, headers=headers)
    import pdb; pdb.set_trace()
    # sess.cookies.set("_UUID_NONLOGIN_", "9ef1c1ffff5148cca3b730354868442e")
    # headers['_UUID_NONLOGIN_'] = "9ef1c1ffff5148cca3b730354868442e"
    # headers['__auc'] = "135d3881cafe4c829f05b4c5ed8dce13"
    # headers['__asc'] = "135d3881cafe4c829f05b4c5ed8dce13"
    # headers['sonic_access_token'] = "135d3881cafe4c829f05b4c5ed8dce13"
    # headers['Cshld-SessionID'] = "135d3881cafe4c829f05b4c5ed8dce13"
    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)
    datares[0]['cookies'] = cookies_new
    return jsonify(datares)


if __name__ == '__main__':
   app.run()

# 135d3881cafe4c829f05b4c5ed8dce13
# 3452078c17ca1ad9badb2b852b2
# b460b788481505d9599cd5dd13ffb47f
# 9ef1c1ffff5148cca3b730354868442e