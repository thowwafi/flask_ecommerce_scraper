import ast
import base64
from datetime import datetime
import json
import os
import pickle
from utils.utils import sleep_time, makeDirIfNotExists
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
import requests


class TokopediaScraper:
    gql_url = "https://gql.tokopedia.com/"
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

    def encode_phone(self, phone):
        """
        Encode phone number with base64
        """
        encoded = base64.b64encode(phone.encode('utf-8'))
        return encoded.decode()  # turn bytes to string

    def get_url(self, phone):
        """
        Generate url from encoded phone number
        """
        phone_enc = self.encode_phone(phone)
        return f"https://accounts.tokopedia.com/otp/c/page?otp_type=112&m_encd={phone_enc}&popup=false&header=true&redirect_parent=false&ld=https%3A%2F%2Faccounts.tokopedia.com%2Flpn%2Fusers%3Fencoded%3D{phone_enc}%26client_id%3D%26redirect_uri%3D%26state%3D"

    def request_otp(self, phone):
        """
        Request OTP by phone
        @phone: phone number
        @return response data
        """
        json_data = json.dumps(self.request_otp_payload(phone))
        sess = requests.Session()
        res = sess.post(self.gql_url, json_data, headers=self.headers)
        return json.loads(res.text)

    def request_otp_payload(self, phone):
        """
        GraphQL query for request OTP
        """
        return [
            {
                "operationName":"OTPRequest","variables":{"msisdn":phone,"otpType":"112","mode":"sms","otpDigit":6},
                "query":"""query OTPRequest($otpType: String!, $mode: String, $msisdn: String, $email: String, $otpDigit: Int, $ValidateToken: String, $UserIDEnc: String) {
                    OTPRequest(otpType: $otpType, mode: $mode, msisdn: $msisdn, email: $email, otpDigit: $otpDigit, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {
                        success
                        message
                        errorMessage
                        sse_session_id
                        list_device_receiver
                        error_code
                        message_title
                        message_sub_title
                        message_img_link
                        __typename
                }\n}\n"""
            }
        ]
    
    def send_otp_payload(self, phone, otp):
        return [{"operationName":"OTPValidate","variables":{"msisdn":phone,"code":otp,"otpType":"112","mode":"sms"},"query":"""query OTPValidate($msisdn: String, $code: String!, $otpType: String, $fpData: String, $getSL: String, $email: String, $mode: String, $ValidateToken: String, $UserIDEnc: String) {
            OTPValidate(code: $code, otpType: $otpType, msisdn: $msisdn, fpData: $fpData, getSL: $getSL, email: $email, mode: $mode, ValidateToken: $ValidateToken, UserIDEnc: $UserIDEnc) {
                success
                message
                errorMessage
                validateToken
                cookieList {
                        key
                    value
                    expire
                    __typename
                }
                __typename
        }\n}\n"""}]

    def account_list_payload(self, phone, validate_token):
        return [{"operationName":"AccountListQuery","variables":{"validate_token":validate_token,"phone":phone,"login_type":""},"query":"""query AccountListQuery($validate_token: String!, $phone: String!, $login_type: String) {
            accountsGetAccountsList(validate_token: $validate_token, phone: $phone, login_type: $login_type) {
                key
                msisdn_view
                msisdn
                users_details {
                    user_id
                    fullname
                    email
                    msisdn_verified
                    image
                    shop_detail {
                    id
                    name
                    domain
                    __typename
                    }
                    challenge_2fa
                    user_id_enc
                    __typename
                }
                users_count
                errors {
                        name
                    message
                    __typename
                }
                __typename
        }\n}\n"""}]

    def send_otp(self, phone, otp):
        """
        Send OTP Number
        @phone: phone number
        @OTP: One-Time Password
        @return: response data
        """
        json_data = json.dumps(self.send_otp_payload(phone, otp))

        sess = requests.Session()
        res = sess.post(self.gql_url, json_data, headers=self.headers)
        data_res_otp = json.loads(res.text)
        validate_token = data_res_otp[0]['data']['OTPValidate']['validateToken']

        json_data_accounts = json.dumps(self.account_list_payload(phone, validate_token))
        res_accounts = sess.post(self.gql_url, json_data_accounts, headers=self.headers)
        data_res_accounts = json.loads(res_accounts.text)
        return data_res_accounts, validate_token

    def create_login_url(self, validate_token, phone):
        phone_enc = self.encode_phone(phone)
        return f"https://accounts.tokopedia.com/lpn/users?encoded={phone_enc}&client_id=&redirect_uri=&state=&validate_token={validate_token}"

    def login_with_email(self, driver, email, login_url, phone):
        base_url = "http://tokopedia.com"
        driver.get(base_url)
        res = requests.get(login_url, headers=self.headers)
        if res.status_code == 403:
            return "Your request is forbidden. Please create new session.", False
        driver.get(login_url)
        sleep_time(2)
        email_choices = driver.find_elements_by_xpath("//p[@class='m-0']")
        if email_choices and email:
            print(email)
            selected_el = [e for e in email_choices if e.text == email]
            if not selected_el:
                return f"Email {email} not found.", False
            selected_el[0].click()
        sleep_time(2)
        driver.get(base_url + "/order-list")
        sleep_time(2)
        sess = requests.Session()
        for cookie in driver.get_cookies():
            sess.cookies.set(cookie['name'], cookie['value'])
        json_data = json.dumps(self.account_payload())
        res = sess.post(self.gql_url, json_data, headers=self.headers)
        datares = json.loads(res.text)
        return datares, True

    def account_payload(self):
        return [{"operationName":"Account","variables":{},"query":"""query Account {
            user {
              id
          isLoggedIn
          name
          profilePicture
          completion
          phoneVerified: phone_verified
          __typename
        }
        userShopInfo {
              info {
                shopId: shop_id
            shopName: shop_name
            shopDomain: shop_domain
            shopAvatar: shop_avatar
            isOfficial: shop_is_official
            __typename
          }
          owner {
                isPowerMerchant: is_gold_merchant
            pmStatus: pm_status
            __typename
          }
          __typename
        }
        wallet {
              ovoCash: cash_balance
          ovoPoints: point_balance
          linked
          __typename
        }
        walletPending: goalPendingBalance {
              pendingBalance: point_balance_text
          __typename
        }
        balance: saldo {
              balanceStr: deposit_fmt
          __typename
        }
        \n}\n"""}]

    def load_session(self, session_token):
        """
        Load cookies into requests session
        """
        cookies = ast.literal_eval(session_token)
        sess = requests.Session()
        for cookie in cookies:
            print(cookie['name'], cookie['value'])
            sess.cookies.set(cookie['name'], cookie['value'])
        return sess

    def get_order_history(self, session, start_at, end_at):
        """
        Retrieve order history
        @start_at
        @end_at
        @return 
        """
        json_data = json.dumps(self.order_history_payload(start_at, end_at))
        res = session.post(self.gql_url, json_data, headers=self.headers)
        return json.loads(res.text)

    def order_history_payload(self, start_at, end_at):
        return [
            {"operationName":"GetOrderHistory","variables":{
                "VerticalCategory":"","Status":"","SearchableText":"","CreateTimeStart":start_at,"CreateTimeEnd":end_at,"Page":1,"Limit":10},
                "query":"""query GetOrderHistory($VerticalCategory: String!, $Status: String!, $SearchableText: String!, $CreateTimeStart: String!, $CreateTimeEnd: String!, $Page: Int!, $Limit: Int!) {
                    uohOrders(input: {UUID: \"\", VerticalID: \"\", VerticalCategory: $VerticalCategory, Status: $Status, SearchableText: $SearchableText, CreateTime: \"\", CreateTimeStart: $CreateTimeStart, CreateTimeEnd: $CreateTimeEnd, Page: $Page, Limit: $Limit, SortBy: \"\", IsSortAsc: false}) {
                    orders {
                        orderUUID
                        verticalID
                        verticalCategory
                        userID
                        status
                        verticalStatus
                        searchableText
                        metadata {
                            upstream
                            verticalLogo
                            verticalLabel
                            paymentDate
                            paymentDateStr
                            queryParams
                            listProducts
                            detailURL {
                                webURL
                                webTypeLink
                                __typename
                            }
                            status {
                                label
                                textColor
                                bgColor
                                __typename
                            }
                            products {
                                title
                                imageURL
                                inline1 {
                                    label
                                    textColor
                                    bgColor
                                    __typename
                                }
                                inline2 {
                                    label
                                    textColor
                                    bgColor
                                    __typename
                                }
                                __typename
                            }
                            otherInfo {
                                actionType
                                appURL
                                webURL
                                label
                                textColor
                                bgColor
                                __typename
                            }
                            totalPrice {
                                value
                                label
                                textColor
                                bgColor
                                __typename
                            }
                            tickers {
                                action {
                                    actionType
                                    appURL
                                    webURL
                                    label
                                    textColor
                                    bgColor
                                    __typename
                                }
                                title
                                text
                                type
                                isFull
                                __typename
                            }
                            buttons {
                                    Label
                                variantColor
                                type
                                actionType
                                appURL
                                webURL
                                __typename
                            }
                            dotMenus {
                                    actionType
                                appURL
                                webURL
                                label
                                textColor
                                bgColor
                                __typename
                            }
                            __typename
                            }
                            createTime
                            createBy
                            updateTime
                            updateBy
                            __typename
                        }
                        totalOrders
                        dateLimit
                        tickers {
                                action {
                                actionType
                            appURL
                            webURL
                            label
                            textColor
                            bgColor
                            __typename
                            }
                            title
                            text
                            type
                            isFull
                            __typename
                        }
                        __typename
                    }
                }
                """
            }
        ]

# TODO
# dibutuhkan untuk setelah otp/login :
# - account _holder
# - account number (bisa no rekening jika bank, no hp untuk e-wallet biasanya)
# untuk retrieval :
# balance dari banks/ewalletnya
# list of transaksi dimana setiap transaksi memiliki :
# value (jumlah income/outcome)
# nama/judul (nama transaksi spr transfer ke x, pembayaran ke x)
# tanggal transaksi
# tipe transkasi ("kredit/debit")
# status transaksi(success or pending or etc)

