import os
import time
import requests
from seleniumwire import webdriver
# from selenium import webdriver
from selenium.webdriver.chrome.options import Options as COptions
from selenium.webdriver.firefox.options import Options as FOptions
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

root_path = os.getcwd()

def interceptor(request):
    del request.headers['sec-fetch-site']
    del request.headers['sec-fetch-mode']
    del request.headers['sec-fetch-dest']
    del request.headers['origin']

    # request.headers["authority"] = "a.m.dana.id"
    # request.headers["method"] = "GET"
    # request.headers["path"] = "/resource/json/ipg/sentry-config.json?params=1636298084834"
    # request.headers["scheme"] = "https"
    request.headers["accept"] = "*/*"
    request.headers["accept-encoding"] = "gzip, deflate, br"
    request.headers["accept-language"] = "en-US,en;q=0.9"
    request.headers["cache-control"] = "no-cache"
    request.headers["origin"] = "https://m.dana.id"
    request.headers["pragma"] = "no-cache"
    request.headers["referer"] = "https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth"
    request.headers["sec-ch-ua"] = '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"'
    request.headers["sec-ch-ua-mobile"] = "?0"
    request.headers["sec-ch-ua-platform"] = "macOS"
    request.headers["sec-fetch-dest"] = "empty"
    request.headers["sec-fetch-mode"] = "cors"
    request.headers["sec-fetch-site"] = "same-site"

def interceptor2(request):
    print("request.headers", request.headers)
def runwebdriver():
    CHROMEDRIVER_PATH = os.path.join(root_path, "chromedriver")
    GECKODRIVER_PATH = os.path.join(root_path, "geckodriver")
    try:
        options = COptions()
        # options.add_argument("--headless")
        options.add_argument('window-size=1920x1080')
        user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"
        options.add_argument(f'user-agent={user_agent}')
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        # options.add_argument("accept=*/*")
        # options.add_argument("accept-encoding=gzip, deflate, br")
        # options.add_argument("accept-language=en-US,en;q=0.9")
        # options.add_argument("cache-control=no-cache")
        # options.add_argument("origin=https://m.dana.id")
        # options.add_argument("pragma=no-cache")
        # options.add_argument("referer=https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth")
        # options.add_argument('sec-ch-ua="Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"')
        # options.add_argument("sec-ch-ua-mobile=?0")
        # options.add_argument("sec-ch-ua-platform=macOS")
        # options.add_argument("sec-fetch-dest=empty")
        # options.add_argument("sec-fetch-mode=cors")
        # options.add_argument("sec-fetch-site=same-site")
        # options.add_argument('--disable-infobars')

        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument(f'user-agent={user_agent}')
        # options.add_argument(f'user-agent={user_agent}')
        d = DesiredCapabilities.CHROME
        d['loggingPrefs'] = { 'browser':'ALL' }
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        options.add_argument("--disable-blink-features=AutomationControlled")
        return webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options, desired_capabilities=d), "Ok"
    except OSError:
        return None, "Mozilla webdriver not matching with OS"
    except Exception as e:
        return None, e
driver, _ = runwebdriver()
# driver.request_interceptor = interceptor
# driver.request_interceptor = interceptor2
driver.get('https://m.dana.id/d/ipg/inputphone?ipgForwardUrl=%2Fd%2Fportal%2Foauth')
time.sleep(5)
test = driver.execute_script("var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;")

for item in test:
    print("item", item)
for entry in driver.get_log('browser'):
    print("entry", entry)
driver.execute_script("return navigator.userAgent")

# Access requests via the `requests` attribute
# for request in driver.requests:
#     if request.response:
#         print(
#             request.url,
#             request.response.status_code,
#             request.response.headers['Content-Type']
#         )



# headers = {
#         "accept-encoding": "gzip, deflate, br",
#         "accept-language": "en-US,en;q=0.9,id;q=0.8",
#         "cache-control": "no-cache",
#         "content-length": "135",
#         "content-type": "application/json",
#         "origin": "https://m.dana.id",
#         "pragma": "no-cache",
#         "sec-ch-ua-mobile": "?0",
#         "sec-ch-ua-platform": "macOS",
#         "sec-fetch-dest": "empty",
#         "sec-fetch-mode": "cors",
#         "sec-fetch-site": "same-site",
#         "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
#     }

# url1 = "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.checkRegisteredUserAndSendOTP.json"

# payload = {
#     "phoneNumber":"62-81272709003",
#     "extParams":{
#         "rdsStandalone":"{\"bizNo\":\"094739e6_4757_4327_a284_11003815108f\",\"antCaptchaToken\":\"4e6e10634a4b4f6e93adac5ac749c6aad8b8a6a48e624d65899b766c582bb88b\",\"rdsScene\":\"nextCheckRegister\"}"
#     }
# }

# session = requests.Session()
# response = session.post(url1, data=payload, headers=headers)

# import pdb; pdb.set_trace()

# [{'name': 'ALIPAYJSESSIONID', 'value': 'GZ00557DFAEE97754119A2AC0F4C82CF23BDaphomeGZ00', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'ctoken', 'value': 'LIgUmYeG8yuq1WJs', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'JSESSIONID', 'value': 'GZ00557DFAEE97754119A2AC0F4C82CF23BDaphomeGZ00', 'path': '/d/ipg', 'domain': 'm.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': '__cf_bm', 'value': 'EPtYVetOsrWxtqIl.amzOxC0th.sS53r.KCeLOiVpAw-1636012461-0-AYteppX+oUTKSqYx2H2xDlo2O4V+FltpOrW7xo/oJmGXqFauAVoQNYNxH+qfIyMneX8tbko05TkLf9Dz+CW8r9k=', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1636014261, 'sameSite': 'None'}, {'name': 'alipay_apdid_token', 'value': '%2FHPzid6N3vyP41DyH1peoB1B%2BZakR%2Fl3sMBTK6aXSniUzBfWMB4OMdAHrrHtBxkV', 'path': '/', 'domain': 'm.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1924905600, 'sameSite': 'None'}, {'name': 'oneDayId', 'value': '3836822981', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1667548467, 'sameSite': 'None'}, {'name': 'mp_ded2d68965bbd813d33d686ee165bae7_mixpanel', 'value': '%7B%22distinct_id%22%3A%20%2217ce9f11a19357-0f70fbb4e1af24-455e6d-13c680-17ce9f11a1bf54%22%2C%22%24device_id%22%3A%20%2217ce9f11a19357-0f70fbb4e1af24-455e6d-13c680-17ce9f11a1bf54%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22App%20Name%22%3A%20%22IPG%22%2C%22Package%20Version%22%3A%20%221.65.0%22%2C%22Package%20Source%22%3A%20%22Online%22%2C%22Package%20Module%22%3A%20%22dana-desktop%22%2C%22__timers%22%3A%20%7B%22OTP%20Input%22%3A%201636012467522%7D%7D', 'path': '/', 'domain': '.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1667548467, 'sameSite': 'None'}]
# [{'name': 'ALIPAYJSESSIONID', 'value': 'GZ00640CB75EBF2144DA8EE132C5F1EB2571aphomeGZ00', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'ctoken', 'value': 'HUPLQJEMzZkJY13N', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'JSESSIONID', 'value': 'GZ00640CB75EBF2144DA8EE132C5F1EB2571aphomeGZ00', 'path': '/d/ipg', 'domain': 'm.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': '__cf_bm', 'value': 'Gy4ptqxGgeDJOeYFUbDWQouxF2cwqGwxyqI7MtWAl8s-1636012355-0-AQw/JOsb9VvJ2B1+vnDPPX1w1qob+bMU75IOvM+KhvVNDKkODx+l1NwvQLwJr0kvX2+sjlEL2XesA/vuQM1x/tA=', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1636014155, 'sameSite': 'None'}, {'name': 'alipay_apdid_token', 'value': 'lXtyeHQd13XvpFJROA9wT5%2B9bC8Q6OHiIGxsidBJTb85CQqIlMq03MfD4YuagMfu', 'path': '/', 'domain': 'm.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1924905600, 'sameSite': 'None'}, {'name': 'oneDayId', 'value': '2363591929', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1667548363, 'sameSite': 'None'}, {'name': 'mp_ded2d68965bbd813d33d686ee165bae7_mixpanel', 'value': '%7B%22distinct_id%22%3A%20%2217ce9ef8e6a534-0d04ab29c4f1448-455e6d-13c680-17ce9ef8e6b687%22%2C%22%24device_id%22%3A%20%2217ce9ef8e6a534-0d04ab29c4f1448-455e6d-13c680-17ce9ef8e6b687%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22App%20Name%22%3A%20%22IPG%22%2C%22Package%20Version%22%3A%20%221.65.0%22%2C%22Package%20Source%22%3A%20%22Online%22%2C%22Package%20Module%22%3A%20%22dana-desktop%22%7D', 'path': '/', 'domain': '.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1667548363, 'sameSite': 'None'}]