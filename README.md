# ecommerce-scraper

## Install requirements
```
pip install -r requirements.txt
```

## Run Flask
```
python app.py
```

## Download Firefox WebDriver
- Download link: https://github.com/mozilla/geckodriver/releases
- Download the appropriate webdriver for your operating system
- Put `geckodriver` in the root path

## Tokopedia API requests
1. Request OTP
```
URL = http://127.0.0.1:5000/api/request_otp/
Method = POST
Body:
{
    "phone": "080989999"
}
Response:
{
    "message": "SMS telah dikirim.",
    "status": "Success",
    "success": true
}
```
2. Send OTP
```
URL = http://127.0.0.1:5000/api/send_otp/
Method = POST
Body:
{
    "phone": "080989999",
    "otp": "501709"
}
Response:
if user have more than 1 account:
{
    "message": "You have 2 different emails please choose one.",
    "status": "Success",
    "user_data": [
        "example1@gmail.com",
        "example2@gmail.com"
    ],
    "validate_token": "c8f6e911b4b74df1ba94c806c806e316"
}
else:
{
    "data": [
        {
            "data": {
                "balance": {
                    "__typename": "Saldo",
                    "balanceStr": "Rp0"
                },
                "user": {},
                "userShopInfo": {},
                "wallet": {},
                "walletPending": {}
            }
        }
    ],
    "message": "Successfully login",
    "session_token": ""
}
```
3. Send validate token and email (Only if user have more than 1 account.)
```
URL = http://127.0.0.1:5000/api/login/
Method = POST
Body:
{
    "phone": "08098999",
    "validate_token": "2f2ff62c6fd54e7084bb17e76407e137",
    "email": "example1@gmail.com"
}
Response:
{
    "data": [
        {
            "data": {
                "balance": {
                    "__typename": "Saldo",
                    "balanceStr": "Rp0"
                },
                "user": {},
                "userShopInfo": {},
                "wallet": {},
                "walletPending": {}
            }
        }
    ],
    "message": "Successfully login",
    "session_token": ""
}
```
4. Get transactions data
```
URL = http://127.0.0.1:5000/api/transaction_list/
Method = POST
Body:
{
    "session_token": "",
    "start_at": "2021-10-01",
    "end_at": "2021-10-29"
}
Response:
{
    "data": [
        {
            "data": {
                "uohOrders": {
                    "__typename": "UOHOrdersResponse",
                    "dateLimit": "2018-09-01",
                    "orders": [],
                    "tickers": [],
                    "totalOrders": 7
                }
            }
        }
    ],
    "message": "Successfully retrieve transactions data.",
    "status": "Success."
}
```

## Dana API requests

1. Request OTP
```
URL = http://127.0.0.1:5000/api/dana/request_otp/
Method = POST
Body:
{
    "phone": "080989999",
    "pin": "999666"
}
Response:
{
    "session_token": "ALIPAYJSESSIONID=GZ0040A647B718CC4F3080F0D3661975E586aphomeGZ00;security_id=sid30f78f844cfa94ddad666ccc5b59ec29_crc&credentials=AxaRpVegFepxIQv7adBijoQvCFEO0XMV6VrGLK45c5pPgHYt4G1i8ZsO%2FrjhDhTLEV%2F8mkLdvJw2w6cMvkkYpBkpbESACsthw51%2Bpoo4mVF5A1MTPq3aSE0c19HXDj5I%2FG04z9RJKXSXruJ5D7823nCy9ovVXKqESPsYmO0CVsGfIhYm0ixUE2623yePgUuwOrWUE2Vv0GmIzx7Bd6ZetcIcfX2QYL6hfCY700XzgLKB1njuZzutFf2wmeEvSNyXMiz9YGMVcFCm16D4aGf80OSduXFaPgjFfsomKwG1KkCIbtJyrsXLCwz0iU15r%2FIUdapf0Q70Y1qfaz33c%2BMPpw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth",
    "status": "Success"
}
```
2. Send OTP
```
URL = http://127.0.0.1:5000/api/dana/send_otp/
Method = POST
Body:
{
    "phone": "080989999",
    "otp": "3641",
    "session_token": "ALIPAYJSESSIONID=GZ0040A647B718CC4F3080F0D3661975E586aphomeGZ00;security_id=sid30f78f844cfa94ddad666ccc5b59ec29_crc&credentials=AxaRpVegFepxIQv7adBijoQvCFEO0XMV6VrGLK45c5pPgHYt4G1i8ZsO%2FrjhDhTLEV%2F8mkLdvJw2w6cMvkkYpBkpbESACsthw51%2Bpoo4mVF5A1MTPq3aSE0c19HXDj5I%2FG04z9RJKXSXruJ5D7823nCy9ovVXKqESPsYmO0CVsGfIhYm0ixUE2623yePgUuwOrWUE2Vv0GmIzx7Bd6ZetcIcfX2QYL6hfCY700XzgLKB1njuZzutFf2wmeEvSNyXMiz9YGMVcFCm16D4aGf80OSduXFaPgjFfsomKwG1KkCIbtJyrsXLCwz0iU15r%2FIUdapf0Q70Y1qfaz33c%2BMPpw%3D%3D&ipgForwardUrl=%2Fd%2Fportal%2Foauth"
}
Response:
{
    "session_token": "__cf_bm=lqFLE1bD.unL3BwMK4d9LbPyG62AWkvlTvRA9lkAIfg-1636730921-0-AZGFhQAIwR6o4rxQi6Lub501XiWNFXzcKo8H1YXvLHUafnu04RWIz9JlnPVZmcZwgQmKXRmpaZYRPaSylOrzRRY=;ALIPAYJSESSIONID=GZ00D70818A24F6E438A8879EAD3F7BB7454aphomeGZ00;",
    "status": "Success"
}
```
3. Get transactions list
```
URL = http://127.0.0.1:5000/api/dana/transactions/
Method = POST
Body:
{
    "session_token": "__cf_bm=lqFLE1bD.unL3BwMK4d9LbPyG62AWkvlTvRA9lkAIfg-1636730921-0-AZGFhQAIwR6o4rxQi6Lub501XiWNFXzcKo8H1YXvLHUafnu04RWIz9JlnPVZmcZwgQmKXRmpaZYRPaSylOrzRRY=;ALIPAYJSESSIONID=GZ00D70818A24F6E438A8879EAD3F7BB7454aphomeGZ00;",
    "start_at": "2021-11-01",
    "end_at": "2021-11-12"
}
Response:
{
    "status": "Success",
    "transactions": {
        ...
    },
    "user": {
        ...
    }
}
```
