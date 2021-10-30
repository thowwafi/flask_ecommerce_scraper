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
```
Download link: https://github.com/mozilla/geckodriver/releases
Download the appropriate webdriver for your operating system
Put `geckodriver` in the root path
```

## API requests
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
{
    "message": "",
    "status": "Success",
    "user_data": {
        ...
        "users_details": [
            {
                "email": "example1@gmail.com",
            },
            {
                "email": "example2@gmail.com",
            }
        ]
    },
    "validate_token": "2f2ff62c6fd54e7084bb17e76407e137"
}
```
3. Send validate token and email
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