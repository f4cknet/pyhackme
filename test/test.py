import requests,time

phones = ["13112345223","13100001111","15230906604","18623106079","13487685476"]
url = "http://127.0.0.1:5000/user/login"
while True:
    for phone in phones:
        for i in range(3):
            data = {"phone":phone,"password":"123"}
            respon = requests.post(url=url,data=data)
            print(respon.text)
            time.sleep(1)