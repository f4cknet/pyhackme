from app.models import db,User
from app.common.argon2hash import argon2hasher
from app.common.sql import ApiSql
import redis,time
from flask import redirect,url_for,session
from functools import wraps


redis_client = redis.Redis(host='localhost',port=6379,db=0)


# def phone_valid(phone):
#     sql = "select * from user where phone='%s'" %(phone)
#     with ApiSql() as s:
#         data = s.read_sql(sql)
#     return data

def login_valid(phone,password):
    data = phone_valid(phone)
    if len(data)>0:
        sql = "select password from user where phone='%s' limit 0,1" %(phone)
        with ApiSql() as s:
            data = s.read_sql(sql)
            query_password_hash = data[0][0]
            print(query_password_hash)
            if argon2hasher(password) == query_password_hash:
                return True
            else:
                return False

def valid_user(phone,password):
    sql = "select password from user where phone='%s' limit 0,1" % (phone)
    print(sql)
    with ApiSql() as s:
        try:
            data = s.read_sql(sql)
            query_password_hash = data[0][0]
            if argon2hasher(password) == query_password_hash:
                return True
            else:
                return False
        except:
            return False
def valid_admin(username,password):
    sql = "select password from admin where username='%s' limit 0,1" % (username)
    print(sql)
    with ApiSql() as s:
        try:
            data = s.read_sql(sql)
            query_password_hash = data[0][0]
            if argon2hasher(password) == query_password_hash:
                return True
            else:
                return False
        except:
            return False

def protect_user_login(phone):
    lockout_time = 60
    max_failed_attempts = 3
    current_round = redis_client.get(f"current_round_{phone}")
    if not current_round:
        current_round = 1
        redis_client.setex(f"current_round_{phone}",lockout_time,1)

    if redis_client.exists(f"locked_{phone}"):
        if int(redis_client.get(f'locked_{phone}')) > int(time.time()):
            return "账号还在锁定中，请稍后尝试"
        redis_client.delete(f"locked_{phone}")

    failed_attempts_key = f"attempts_{phone}_round_{current_round}"
    failed_attempts = redis_client.get(failed_attempts_key)
    if failed_attempts and int(failed_attempts) >= max_failed_attempts:
        # 锁定用户操作
        redis_client.setex(f"locked_{phone}", lockout_time, int(time.time()) + lockout_time)

        # 增加轮数
        current_round = int(current_round)
        current_round+=1
        redis_client.setex(f"current_round_{phone}",lockout_time,current_round)

        # 重置失败尝试次数
        redis_client.delete(failed_attempts_key)
        return "账号被锁定中"

    return None

def vaild_email_phone(email,phone):
    query_phone = db.session.query(User.phone).filter_by(email=email).first()
    result_phone = query_phone[0]
    if result_phone == phone:
        return True
    else:
        return False

def is_login(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "username" not in session:
            return redirect(url_for('admin.login'))
        else:
            return func(*args,**kwargs)
    return wrapper

def user_is_login(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if "phone" not in session:
            return redirect(url_for('user.login'))
        else:
            return func(*args,**kwargs)
    return wrapper

if __name__ == "__main__":
    valid("15311111111'+or+'1'='1","123")
    # login_valid("13112345223","1231123123")