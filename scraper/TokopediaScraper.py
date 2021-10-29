import base64
from datetime import datetime
import json
import os
import pickle
import requests
from utils.utils import sleep_time, makeDirIfNotExists


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


class TokopediaScraper:
    def __init__(self, phone=""):
        self.phone = phone
        self.encoded_phone = self.encode_phone()
        self.url = self.get_url()

    def encode_phone(self):
        """
        Encode phone number with base64
        """
        encoded = base64.b64encode(self.phone.encode('utf-8'))
        return encoded.decode()  # turn bytes to string

    def get_url(self):
        """
        Generate url from encoded phone number
        """
        return f"https://accounts.tokopedia.com/otp/c/page?otp_type=112&m_encd={self.encoded_phone}&popup=false&header=true&redirect_parent=false&ld=https%3A%2F%2Faccounts.tokopedia.com%2Flpn%2Fusers%3Fencoded%3D{self.encoded_phone}%26client_id%3D%26redirect_uri%3D%26state%3D"

    def request_otp(self, driver):
        """
        Send GET request to URL to get OTP
        """
        driver.get(self.url)
        sleep_time(2)
        driver.find_element_by_id("cotp__method--sms").click()
        sleep_time(2)
        driver.quit()

    def send_otp(self, driver, otp, email):
        """
        Send OTP Number
        """
        driver.get(self.url)
        sleep_time(2)
        driver.find_element_by_id("cotp__method--sms").click()
        sleep_time(2)
        for index, number in enumerate(otp, start=1):
            driver.find_element_by_id(f"otp-number-input-{index}").send_keys(number)
        sleep_time(2)
        email_choices = driver.find_elements_by_xpath("//p[@class='m-0']")
        if email_choices and email:
            selected_el = [e for e in email_choices if e.text == email]
            selected_el[0].click()
        sleep_time(2)

        gql_url = "https://gql.tokopedia.com/"
        sess = requests.Session()
        for cookie in driver.get_cookies():
            sess.cookies.set(cookie['name'], cookie['value'])
        json_data = json.dumps(self.account_payload())
        gql_url = "https://gql.tokopedia.com/"
        res = sess.post(gql_url, json_data, headers=headers)
        datares = json.loads(res.text)

        web_url = "http://tokopedia.com"
        driver.get(web_url + "/order-list")
        sleep_time(2)
        return datares

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

    def create_session_id(self):
        return datetime.now().strftime("%Y%m%d%H%M%S")
    
    def save_session(self, root_path, driver):
        session_id = self.create_session_id()
        cookies_folder = os.path.join(root_path, 'cookies')
        makeDirIfNotExists(cookies_folder)
        cookie_file = os.path.join(cookies_folder, f"cookies_{session_id}.pkl")
        pickle.dump(driver.get_cookies(), open(cookie_file, "wb"))
        return session_id

    def load_session(self, session_id, root_path):
        """
        Load saved cookies by session_id
        """
        cookies_folder = os.path.join(root_path, 'cookies')
        cookie_file = os.path.join(cookies_folder, f"cookies_{session_id}.pkl")
        return pickle.load(open(cookie_file, "rb"))

    def load_cookies(self, cookies):
        """
        Load cookies into requests session
        """
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
        gql_url = "https://gql.tokopedia.com/"
        res = session.post(gql_url, json_data, headers=headers)
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
                        filtersV2 {
                                label
                            value
                            isPrimary
                            __typename
                        }
                        categories {
                                value
                            label
                            __typename
                        }
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