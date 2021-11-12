from flask import Flask
from flask import request, jsonify
import requests
from scraper.TokopediaScraper import TokopediaScraper
from scraper.DanaScraper import DanaScraper
from utils.utils import initialize_webdriver


app = Flask(__name__)
app.config["DEBUG"] = True

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
        login_data, ok = tokped.login_with_email(driver, None, login_url, phone)
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
    driver, message = initialize_webdriver(app.root_path)

    response = {}
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500

    dana = DanaScraper()
    security_id = dana.request_otp(driver, phone, pin)

    cookies = [i for i in driver.get_cookies() if i.get('name') == 'ALIPAYJSESSIONID']
    token = f"{cookies[0]['name']}={cookies[0]['value']};security_id={security_id}"

    response['status'] = 'Success'
    response['session_token'] = f"{token}"
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

    dana = DanaScraper()
    session_token, security_id = dana.split_session_token(session_token_plus)

    response = {}
    driver, message = initialize_webdriver(app.root_path)
    if not driver:
        response['message'] = str(message)
        response['status'] = 'Failed'
        return jsonify(response), 500
    
    login_cookie = dana.send_otp(driver, security_id, otp, session_token, phone)
    response['status'] = 'Success'
    response['session_token'] = login_cookie
    driver.quit()
    return jsonify(response)


@app.route('/api/dana/transactions/', methods=['POST'])
def dana_transactions():
    request_data = request.json
    session_token = request_data.get('session_token')

    response = {}
    dana = DanaScraper()
    data = dana.get_transactions(session_token)
    response['status'] = 'Success'
    response['data'] = data
    return jsonify(response)

if __name__ == '__main__':
   app.run()
