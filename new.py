import base64
import hashlib

no = "087877544953"
encoded = base64.b64encode(no.encode('utf-8'))
dec = encoded.decode()
print(dec)

# mypass = "Alpiphysics_27"
# string = base64.b64encode(mypass.encode('utf-8'))
# password = hashlib.md5(string).hexdigest()
url = f"https://accounts.tokopedia.com/otp/c/page?otp_type=112&m_encd={dec}&popup=false&header=true&redirect_parent=false&ld=https%3A%2F%2Faccounts.tokopedia.com%2Flpn%2Fusers%3Fencoded%3D{dec}%26client_id%3D%26redirect_uri%3D%26state%3D"
print(url)
# MDgxMjcyNzA5MDAz
email_url = f"https://accounts.tokopedia.com/lpn/users?encoded={dec}&client_id=&redirect_uri=&state=&validate_token=ec682fe57742470b801d95a2da3021d8"
print(email_url)
# 294f3426c27d4273af3bc729ed8ad84c
# https://accounts.tokopedia.com/lpn/users?encoded=MDg3ODc3NTQ0OTUz&client_id=&redirect_uri=&state=&validate_token=294f3426c27d4273af3bc729ed8ad84c