import time
import asyncio

import requests
url = "http://127.0.0.1:8000/user/login"

account = ['13100001111','13100002222','15230906604']


async def attack_hackme():
    num = 0
    while True:
        for item in account:
            res = requests.post(url=url,data={"phone":item,"password":"9ijn8uubhh"})
            print(res.text)
            print(item)
        num+=1
        if num >3:
            time.sleep(60)
            num =0

asyncio.run(attack_hackme())
