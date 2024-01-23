## Pyhackme

[中文](README.md)

#### Approached to real-world vulnerability application

> Different from most web vulnerability application the market, pyhackme is closer to real business scenarios. The business scenarios corresponding to each vulnerability are true portrayals of vulnerabilities that have been dug.

###  vulnerability list

##### 1. authentication
```buildoutcfg
1. register：User registration prompts that the user already exists and user enumeration can be performed

2. login

   2.1 The business system made unreasonable security designs for failed logins, leading to account denial of service attacks.

   2.2 The business system uses a slow hash function, which allows users to be enumerated by observing the response time and SQL injection.（not using sleep() or benchmark,just slow hash function）

3. retrieves passwod：Host injection occurs when retrieving the password, resulting in account takeover

4. admin login：Since the administrator backend did not perform login failure verification, the administrator account was enumerated based on 2.2, and then the password was violently cracked.
```


##### 2. SSRF
```buildoutcfg
1. Batch import of products in the background: The excel file of the product is first transferred to the storage object, and then the server initiates a request to obtain the file for import. The requested URL is controllable, leading to SSRF vulnerability.
```

##### 3. CSRF
```buildoutcfg
1. Payment function：Use the balance of other people’s accounts to pay for yourself
2. Add admin account
```
##### 4. SQLI
```buildoutcfg
1. login：Boolean SQLi
2. order detail：Union SQLi
```

##### 5. race condition
```buildoutcfg
1. Stored value card recharge：A stored-value card can be recharged multiple times
```

##### 6. unauthorized access
```buildoutcfg
1. Repurchase：Repeated purchases beyond your authority, consuming other people’s account balances
2. Consignee management
   2.1 Modifying consignee information beyond your authority
   2.2 View consignee information beyond your authority
3. view order detail：Viewing other people’s order information beyond their authority
4. Refund：Unauthorized refunds may lead to disputes between buyers and sellers, as well as other adverse effects.
```


#### 使用
```buildoutcfg
1. environment：python3+mysql+redis
2. dependencies：pip install -r requirements.txt
3. Modify app/config.py configuration information
   3.1 ossak：Aliyun accesskey
   3.2 osssk：Aliyun secretkey
   3.3 SQLALCHEMY_DATABASE_URI： Database connection address
   3.4 SECRET_KEY： any string
   3.5 MAIL_SERVER：smtp server
   3.6 MAIL_PORT:  smpt port
   3.7 MAIL_USE_SSL:  use ssl or not
   3.8 MAIL_USERNAME ： sender
   3.9 MAIL_PASSWORD ：sender password
   3.10 MAIL_DEFAULT_SENDER：sender
4. database init
   4.1 flask db init
   4.2 flask db migrate
   4.3 flask upgrade
5. app run： flask run -h 0.0.0.0
```

![](./screenhot/1.jpg)

have fun!




