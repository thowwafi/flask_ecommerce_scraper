import requests


headers = {
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9,id;q=0.8",
        "cache-control": "no-cache",
        "content-length": "135",
        "content-type": "application/json",
        "origin": "https://m.dana.id",
        "pragma": "no-cache",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "macOS",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

url1 = "https://m.dana.id/wallet/api/alipayplus.mobilewallet.user.checkRegisteredUserAndSendOTP.json"

payload = {
    "phoneNumber":"62-81272709003",
    "extParams":{
        "rdsStandalone":"{\"bizNo\":\"094739e6_4757_4327_a284_11003815108f\",\"antCaptchaToken\":\"4e6e10634a4b4f6e93adac5ac749c6aad8b8a6a48e624d65899b766c582bb88b\",\"rdsScene\":\"nextCheckRegister\"}"
    }
}

session = requests.Session()
response = session.post(url1, data=payload, headers=headers)

import pdb; pdb.set_trace()

[{'name': 'ALIPAYJSESSIONID', 'value': 'GZ00557DFAEE97754119A2AC0F4C82CF23BDaphomeGZ00', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'ctoken', 'value': 'LIgUmYeG8yuq1WJs', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'JSESSIONID', 'value': 'GZ00557DFAEE97754119A2AC0F4C82CF23BDaphomeGZ00', 'path': '/d/ipg', 'domain': 'm.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': '__cf_bm', 'value': 'EPtYVetOsrWxtqIl.amzOxC0th.sS53r.KCeLOiVpAw-1636012461-0-AYteppX+oUTKSqYx2H2xDlo2O4V+FltpOrW7xo/oJmGXqFauAVoQNYNxH+qfIyMneX8tbko05TkLf9Dz+CW8r9k=', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1636014261, 'sameSite': 'None'}, {'name': 'alipay_apdid_token', 'value': '%2FHPzid6N3vyP41DyH1peoB1B%2BZakR%2Fl3sMBTK6aXSniUzBfWMB4OMdAHrrHtBxkV', 'path': '/', 'domain': 'm.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1924905600, 'sameSite': 'None'}, {'name': 'oneDayId', 'value': '3836822981', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1667548467, 'sameSite': 'None'}, {'name': 'mp_ded2d68965bbd813d33d686ee165bae7_mixpanel', 'value': '%7B%22distinct_id%22%3A%20%2217ce9f11a19357-0f70fbb4e1af24-455e6d-13c680-17ce9f11a1bf54%22%2C%22%24device_id%22%3A%20%2217ce9f11a19357-0f70fbb4e1af24-455e6d-13c680-17ce9f11a1bf54%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22App%20Name%22%3A%20%22IPG%22%2C%22Package%20Version%22%3A%20%221.65.0%22%2C%22Package%20Source%22%3A%20%22Online%22%2C%22Package%20Module%22%3A%20%22dana-desktop%22%2C%22__timers%22%3A%20%7B%22OTP%20Input%22%3A%201636012467522%7D%7D', 'path': '/', 'domain': '.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1667548467, 'sameSite': 'None'}]
[{'name': 'ALIPAYJSESSIONID', 'value': 'GZ00640CB75EBF2144DA8EE132C5F1EB2571aphomeGZ00', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'ctoken', 'value': 'HUPLQJEMzZkJY13N', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': 'JSESSIONID', 'value': 'GZ00640CB75EBF2144DA8EE132C5F1EB2571aphomeGZ00', 'path': '/d/ipg', 'domain': 'm.dana.id', 'secure': True, 'httpOnly': True, 'sameSite': 'None'}, {'name': '__cf_bm', 'value': 'Gy4ptqxGgeDJOeYFUbDWQouxF2cwqGwxyqI7MtWAl8s-1636012355-0-AQw/JOsb9VvJ2B1+vnDPPX1w1qob+bMU75IOvM+KhvVNDKkODx+l1NwvQLwJr0kvX2+sjlEL2XesA/vuQM1x/tA=', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1636014155, 'sameSite': 'None'}, {'name': 'alipay_apdid_token', 'value': 'lXtyeHQd13XvpFJROA9wT5%2B9bC8Q6OHiIGxsidBJTb85CQqIlMq03MfD4YuagMfu', 'path': '/', 'domain': 'm.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1924905600, 'sameSite': 'None'}, {'name': 'oneDayId', 'value': '2363591929', 'path': '/', 'domain': '.m.dana.id', 'secure': True, 'httpOnly': True, 'expiry': 1667548363, 'sameSite': 'None'}, {'name': 'mp_ded2d68965bbd813d33d686ee165bae7_mixpanel', 'value': '%7B%22distinct_id%22%3A%20%2217ce9ef8e6a534-0d04ab29c4f1448-455e6d-13c680-17ce9ef8e6b687%22%2C%22%24device_id%22%3A%20%2217ce9ef8e6a534-0d04ab29c4f1448-455e6d-13c680-17ce9ef8e6b687%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%2C%22App%20Name%22%3A%20%22IPG%22%2C%22Package%20Version%22%3A%20%221.65.0%22%2C%22Package%20Source%22%3A%20%22Online%22%2C%22Package%20Module%22%3A%20%22dana-desktop%22%7D', 'path': '/', 'domain': '.dana.id', 'secure': False, 'httpOnly': False, 'expiry': 1667548363, 'sameSite': 'None'}]