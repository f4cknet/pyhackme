## 密码学
对称加密算法
非对称加密算法
散列函数：md5，md4，sha1，sha2-256，sha2-126，sha3-512
Hmacmd5，hmacsha256

慢散列函数：argon

md5(adminadmindamiadnadminadmindaindamiadnadminadmindamiadnadminadmindamiadn)
0.001ms

hmacsha256(adminadmindamiadnadminadmindaindamiadnadminadmindamiadnadminadmindamiadn)
0.01ms

argon2(adminadmindamiadnadminadmindaindamiadnadminadmindamiadnadminadmindamiadn)
10ms

pip install argon2_cffi

abc
def
ghij
klm
nopqrstuvwxyz

dblength =6
dbname1 = h
dbname2 = a
dbname3 = c
dbname4 = k
dbname5 = m
dbname6 = e

dbname: hackme

current database: 'hackme'
table: user

select password from user where phone='-1111' limit 0,1

locked_{phone}
current_round_{phone} 1
attempts_{phone}_round_current_round_{phone}>=3:
    setex(f"locked_{phone}")





