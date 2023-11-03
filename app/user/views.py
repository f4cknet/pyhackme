from flask import Blueprint,request,render_template
from app.models import User,db
from app.common.argon2hash import argon2hasher
from app.common.authen import valid_user,redis_client,protect_user_login

user = Blueprint('user',__name__,url_prefix='/user')

# @user.route('/detail',methods=["GET","POST"])
# def detail():
#     if request.method == "GET":
#         if request.args.get("username"):
#             username = request.args.get("username")
#             return username
#         else:
#             return "没用username参数"

@user.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        #注册逻辑
        phone = request.form.get('phone')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            return '两次密码不一致，重新注册'
        try:
            password_hash = argon2hasher(password)
            user = User(phone=phone, email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()
            return "注册成功"
        except Exception as e:
            return "已存在该用户"
            db.session.rollback()
            raise e
        else:
            return "两次密码不一致，重新注册"

    return render_template("/user/register.html")

@user.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        phone = request.form.get('phone')
        password = request.form.get('password')
        lock_msg = protect_user_login(phone)
        if lock_msg:
            return lock_msg

        result = valid_user(phone,password)
        if result is True:
            return "登陆成功"
        elif result is False:
            lockout_time = 60
            current_round = redis_client.get(f'current_round_{phone}')
            failed_attempts_key = f"attempts_{phone}_round_{current_round}"
            if redis_client.exists(failed_attempts_key):
                redis_client.incr(failed_attempts_key)
            else:
                redis_client.setex(failed_attempts_key,lockout_time,1)
            return "登陆失败"




    return render_template('user/login.html')
