from flask import Flask
from flask import request, jsonify
from flask import Response
import json
import os
from pprint import pprint
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import sys


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

CHROMEDRIVER_PATH = os.path.join(app.root_path, "chromedriver")
def check_chrome_driver():
    try:
        options = Options()
        # options.add_argument("--headless")
        return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    except OSError:
        sys.exit("Chrome webdriver not matching with OS")
    except Exception as e:
        sys.exit(str(e))

def create_response(message, status):
    return jsonify({
        "message": message,
        "status": status
    })


@app.route('/api/login/', methods=['POST'])
def login():
    request_data = request.json

    if "phone" not in request_data:
        return jsonify({"message": "Phone cannot be blank."}), 400

    phone = request_data.get('phone')
    if phone is None:
        return jsonify({"message": "Phone cannot be null."}), 400
    phone = phone.strip()
    if not phone:
        return jsonify({"message": "Phone cannot be null."}), 400

    payload = [{"operationName":"OTPRequest","variables":{"msisdn":phone,"otpType":"112","mode":"sms","otpDigit":6},"query":"query OTPRequest($otpType: String!, $mode: String, $msisdn: String, $email: String, $otpDigit: Int, $ValidateToken: String, $UserIDEnc: String) {\n  OTPRequest(otpType: $otpType, mode: $mode, msisdn: $msisdn, email: $email, otpDigit: $otpDigit, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {\n    success\n    message\n    errorMessage\n    sse_session_id\n    list_device_receiver\n    error_code\n    message_title\n    message_sub_title\n    message_img_link\n    __typename\n  }\n}\n"}]
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
        response['cookies'] = cookies_new
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

    # cookies =  {
    #     "_abck": "7BB9502BBA6876269D20424DB57EC722~-1~YAAQJOwZuBVP0ld8AQAALMuAngZhWRath1VmoCXhlbYDn3Kbiijoieuar28kfzAyRE47sQDoWQNliLtRYZU1a0fySuRZxZfkm69Y1QU5SOeuKu1Mwf9PceohOvkkTXpL3uA3pyxwqECm7//a46USviaNy2H2j5Ub3nOXrAQr84UGT83WyxLpoN+pIR39FgO3ePWZU4VeJv4heS/ueiCxj27HowP6/8YCzlMUatqgkjNamVg22Z546Nv75dX8RQ8oyN585C9HEnWZHVtMxRt9/mp0l+Jzgv9nYIDfO+ZcsXfvlu087JHSkaBdJymk0usThjmQ3hJobtSQfzOsUTosu2bsNHsNgZ8tnUXRgJbJu0UanfrQaBELkynWFIpqCh8=~-1~-1~-1",
    #     "ak_bmsc": "6A695B6D78744FEF4FA030D28CDD1355~000000000000000000000000000000~YAAQJOwZuBZP0ld8AQAALMuAng0oe01AM63dvww+f4/QCjGNxG//R/uWMt723bDyy1QuErIeh6sontremIIs1h5GPCMoVNgMIgkStsHKSpCXozUZQnX6C+5rj2GLPK9eA7qw/ng/7n9eoVF4H78k9Q7+L9u61Nh11K9lUixvTlO+cI+0Do+Imvy3eEuADRB6Rs62wlcplZZjeHO5lLihl7mrkjCP7d87W5krAts2S7aXk89O2Osb83hPQRWDUHrnHr8r+p7yCljbEpjwpONTwdDto7X4QNfkpjo089xNYq3+swBjHqvqNslqJCbuy2ldlC2vbb4XyKQe9WmYQFiGKUncWQyhC0eYeT1cQ/keNmAOWLSE10DEjuGMu4a1ksdUOYY=",
    #     "bm_sz": "9BD27047775C9BFA0A909DF8393650BD~YAAQJOwZuBdP0ld8AQAALMuAng1f71mTlPI0K4QLWsKCrDiI+zwPF2HznGSlFuS6l0NI41xXeMveuh6y1AT8QGuLxgNo6QuD/pjSBLnN4gPGGkz5Grsua/AQnUAkCAmiKh6/QX5ve8VYNNBZzTOgl9CUwOCj7gdd5GAYDHRdWtajUO58FkyHe5NGRrw2ZBACYNlzhPiuSsksQmACa0Fpp5q4hyJU5+GryXuz1t/xIHe6/T+H8Fq4OGQylJheK/eG5J0T17Kk6uLVhCzvb0EkuNoMi90VWPCBvw7JaV5emLiQDRN1L0M=~4403252~3224132",
    #     "uid": "rBX7M2FwQbx58UG7AwNeAg=="
    # }
    payload = [{"operationName":"OTPValidate","variables":{"msisdn":phone,"code":otp,"otpType":"112","mode":"sms"},"query":"query OTPValidate($msisdn: String, $code: String!, $otpType: String, $fpData: String, $getSL: String, $email: String, $mode: String, $ValidateToken: String, $UserIDEnc: String) {\n  OTPValidate(code: $code, otpType: $otpType, msisdn: $msisdn, fpData: $fpData, getSL: $getSL, email: $email, mode: $mode, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {\n    success\n    message\n    errorMessage\n    validateToken\n    cookieList {\n      key\n      value\n      expire\n      __typename\n    }\n    __typename\n  }\n}\n"}]
    json_data = json.dumps(payload)

    sess = requests.Session()
    for key, value in cookies.items():
        sess.cookies.set(key, value)

    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)
    print("datares", datares)

    # payload = [{"operationName":"isAuthenticatedQuery","variables":{},"query":"query isAuthenticatedQuery {\n  isAuthenticated\n}\n"}]
    # json_data = json.dumps(payload)
    # res = sess.post(url, json_data, headers=headers)
    
    datares[0]['cookies'] = cookies_new
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
    for key, value in cookies.items():
        sess.cookies.set(key, value)

    res = sess.post(url, json_data, headers=headers)
    cookies_new = sess.cookies.get_dict()
    datares = json.loads(res.text)

    datares[0]['cookies'] = cookies_new
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