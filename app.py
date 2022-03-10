from flask import Flask
from flask import request, jsonify
import requests
from scraper.TokopediaScraper import TokopediaScraper
from scraper.DanaScraper import DanaScraper
from scraper.BukalapakScraper import BukalapakScraper
from utils.utils import initialize_webdriver


app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/')
def hello_world():
    print(app.root_path)
    return "Hello World"

@app.route('/api/request_otp_by_email/', methods=['POST'])
def request_otp_by_email():
    """
    @Body: 
    {
        "email": "someone@gmail.com",
        "password": "password"
    }
    """
    request_data = request.json
    email = request_data.get('email')
    password = request_data.get('password')
    response = {}
    if not email or not password:
        response['status'] = 'Failed'
        response['message'] = 'Email and password cannot be null'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500
    tokped = TokopediaScraper()
    try:
        data_res = tokped.request_otp_by_email(driver, email, password)
    except Exception as e:
        response['status'] = 'Failed'
        response['message'] = str(e)
        return jsonify(response), 500
    driver.quit()
    response = data_res
    response['status'] = 'Success'
    
    return jsonify(response)


@app.route('/api/send_otp_by_email/', methods=['POST'])
def send_otp_by_email():
    """
    @Body:
    {
        "validate_token": "",
        "otp": "627091"
    }
    """
    request_data = request.json
    otp = request_data.get('otp')
    validate_token = request_data.get('validate_token')

    response = {}
    if not validate_token or not otp:
        response['status'] = 'Failed'
        response['message'] = 'Login Token/OTP cannot be null'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500
    tokped = TokopediaScraper()
    try:
        login_data, ok = tokped.send_otp_by_email(driver, otp, validate_token=validate_token)
    except Exception as e:
        response['status'] = 'Failed'
        response['message'] = str(e)
        return jsonify(response), 500
    if not ok:
        response['message'] = str(login_data)
        response['status'] = 'Failed'
        return jsonify(response), 500

    try:
        session_token = tokped.get_session_token(driver)
    except Exception as e:
        response['message'] = "Session ID error. {e}"
        response['status'] = 'Failed'
        return jsonify(response), 500

    response = {
        "message": "Successfully login",
        "session_token": session_token,
        "data": login_data
    }
    driver.quit()
    return jsonify(response)


@app.route('/api/request_otp/', methods=['POST'])
def request_otp():
    """
    @Body: 
    {
        "phone": "080989999",
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
    pin = request_data.get('pin')

    response = {}
    if not phone or not otp:
        response['status'] = 'Failed'
        response['message'] = 'Phone/OTP/PIN cannot be null'
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

    users_details = data_res[0]['data']['accountsGetAccountsList']['users_details']
    count_users = len(users_details)
    if  count_users > 1:
        response["status"] = "Success"
        response["message"] = f"You have {count_users} different emails please choose one."
        response["validate_token"] = validate_token
        response["user_data"] = [user.get('email') for user in users_details]
        return jsonify(response)

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    login_url = tokped.create_login_url(validate_token, phone)
    try:
        login_data, ok = tokped.login_with_email(driver, None, login_url, phone, pin)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'Failed'
        return jsonify(response), 500
    if not ok:
        response['message'] = str(login_data)
        response['status'] = 'Failed'
        return jsonify(response), 500

    try:
        session_token = tokped.get_session_token(driver)
    except Exception as e:
        response['message'] = "Session ID error. {e}"
        response['status'] = 'Failed'
        return jsonify(response), 500

    response = {
        "message": "Successfully login",
        "session_token": session_token,
        "data": login_data
    }
    driver.quit()
    return jsonify(response)


@app.route('/api/login/', methods=['POST'])
def login():
    request_data = request.json
    phone = request_data.get('phone')
    validate_token = request_data.get('validate_token')
    email = request_data.get('email')
    pin = request_data.get('pin')
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
        login_data, ok = tokped.login_with_email(driver, email, login_url, phone, pin)
    except Exception as e:
        response['message'] = str(e)
        response['status'] = 'Failed'
        return jsonify(response), 500
    if not ok:
        response['message'] = str(login_data)
        response['status'] = 'Failed'
        return jsonify(response), 500

    try:
        session_token = tokped.get_session_token(driver)
    except Exception as e:
        response['message'] = "Session ID error. {e}"
        response['status'] = 'Failed'
        return jsonify(response), 500

    response = {
        "message": "Successfully login",
        "session_token": session_token,
        "data": login_data
    }
    driver.quit()
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


@app.route('/api/dana/request_otp/', methods=['POST'])
def dana_request_otp():
    request_data = request.json
    phone = request_data.get('phone')
    if phone.startswith('0'):
        phone = phone[1:]
    pin = request_data.get('pin')

    response = {}
    if not phone or not pin:
        response['message'] = "phone and pin cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    dana = DanaScraper()
    security_id, ok = dana.request_otp(driver, phone, pin)
    if not ok:
        response['message'] = security_id + " Salah PIN 3 kali akan membuat akun anda terblokir selama 1 jam."
        response['status'] = 'Failed'
        response['error_code'] = 'INVALID_CREDENTIALS'
        driver.quit()
        return jsonify(response), 400

    cookies = [i for i in driver.get_cookies() if i.get('name') == 'ALIPAYJSESSIONID']
    if not cookies:
        response['message'] = "ALIPAYJSESSIONID not found."
        response['status'] = 'Failed'
        return jsonify(response), 500
    token = f"{cookies[0]['name']}={cookies[0]['value']};security_id={security_id}"

    response['status'] = 'Success'
    response['session_token'] = token
    driver.quit()
    return jsonify(response)


@app.route('/api/dana/send_otp/', methods=['POST'])
def dana_send_otp():
    request_data = request.json
    phone = request_data.get('phone')
    if phone.startswith('0'):
        phone = phone[1:]
    otp = request_data.get('otp')
    session_token_plus = request_data.get('session_token')

    response = {}
    if not phone or not otp or not session_token_plus:
        response['message'] = "phone, otp, pin, session_token cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    dana = DanaScraper()
    session_token, security_id = dana.split_session_token(session_token_plus)

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500
    
    login_cookie, ok = dana.send_otp(driver, security_id, otp, session_token, phone)
    if not ok:
        response['message'] = login_cookie
        response['status'] = 'Failed'
        response['error_code'] = 'INVALID_OTP'
        driver.quit()
        return jsonify(response), 400
    response['status'] = 'Success'
    response['session_token'] = login_cookie
    driver.quit()
    return jsonify(response)


@app.route('/api/dana/transactions/', methods=['POST'])
def dana_transactions():
    request_data = request.json
    session_token = request_data.get('session_token')
    start_at = request_data.get('start_at')
    end_at = request_data.get('end_at')

    response = {}
    if not session_token or not start_at or not end_at:
        response['message'] = "session_token, start_at, end_at cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    dana = DanaScraper()
    start_date, end_date = dana.convert_date(start_at, end_at)
    res = dana.get_transactions(session_token, start_date, end_date)
    if res.status_code != 200:
        response['message'] = "Token unauthorized."
        response['status'] = 'Failed'
        return jsonify(response), res.status_code

    if not res.json().get('result').get('success'):
        response['status'] = 'Failed'
        response['message'] = res.json().get('result').get('errorMsg')
        response['error_code'] = 'SESSION_EXPIRED'
        return jsonify(response), res.status_code

    res_user = dana.get_user_info(session_token)
    response['status'] = 'Success'
    response['transactions'] = res.json()
    response['user'] = res_user.json()
    return jsonify(response)


@app.route('/api/bl/request_otp/', methods=['POST'])
def bl_request_otp():
    request_data = request.json
    phone = request_data.get('phone')

    response = {}
    if not phone:
        response['message'] = "phone cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    bl = BukalapakScraper()
    cookies = bl.request_otp(driver, phone)

    response['status'] = 'Success'
    response['session_token'] = str(cookies)
    driver.quit()
    return jsonify(response)


@app.route('/api/bl/send_otp/', methods=['POST'])
def bl_send_otp():
    request_data = request.json
    phone = request_data.get('phone')
    otp = request_data.get('otp')
    session_token = request_data.get('session_token')

    response = {}
    if not phone or not otp or not session_token:
        response['message'] = "phone, otp, session_token cannot be null."
        response['status'] = 'Failed'
        return jsonify(response), 400

    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    bl = BukalapakScraper()
    cookies = bl.send_otp(driver, otp, session_token, phone)

if __name__ == '__main__':
   app.run()
