from flask import Blueprint,request,render_template,current_app,session
from app.models import User,db,Goods,Address
from app.common.argon2hash import argon2hasher
from app.common.authen import valid_user,redis_client,protect_user_login,vaild_email_phone,user_is_login
from uuid import uuid4
from flask_mail import Message


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
            session['phone'] = phone
            return "恭喜你，登陆成功"
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

@user.route('/fotgotpassword',methods=["POST","GET"])
def forgot_passowrd():
    if request.method == "POST":
        email = request.form.get('email')
        phone = request.form.get('phone')
        if vaild_email_phone(email,phone):
            randomuid = str(uuid4())
            redis_client.setex(randomuid,600,email)
            url = f"/user/resetpassword/{randomuid}"
            host = request.host

            reset_url = f"http://{host}{url}"
            resetpassword_email = f"请点击一下链接进行密码重置：<a href='{reset_url}'>{reset_url}</a>, 有效期10分钟"
            message = Message(recipients=[email],subject="hackme重置密码")
            message.html =  resetpassword_email
            mail = current_app.extensions['mail']
            mail.send(message)
            return "密码重置链接已发送至您的邮箱，请点击邮箱中的链接进行密码重置"

        else:
            return "邮箱和用户名验证未通过"
    return render_template('user/forgotpassword.html')

@user.route('/resetpassword/<string:randomuid>',methods=["POST","GET"])
def reset_password(randomuid):
    # email = redis_client.get(randomuid)
    if request.method == "GET":
        if redis_client.exists(randomuid):
            email = redis_client.get(randomuid).decode('utf-8')
            return render_template('user/resetpassword.html',email=email,randomuid=randomuid)
        else:
            return render_template('user/resetpassword.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        password1 = request.form.get('confirm_password')
        if redis_client.exists(randomuid):
            redis_email = redis_client.get(randomuid).decode('utf-8')
            print(redis_email,email)
            if email == redis_email:
                if password!=password1:
                    return "两次输入的密码不一样，请检查"
                else:
                    password_hash = argon2hasher(password)
                    User.query.filter_by(email=email).update({"password":password_hash})
                    db.session.commit()

                    return "密码重置成功"
            else:
                return "您没有权限重置该账号密码"
        else:
            return "重置密码链接失效，请重新回到忘记密码页面进行操作"

@user.route('/shoplist',methods=['GET','POST'])
def shoplist():
    goods_lists = db.session.query(Goods).all()
    return render_template('/user/goods_lists.html',goods_lists=goods_lists)



@user.route('/order',methods=['GET','POST'])
@user_is_login
def order():
    goodsid = request.args.get('goodsid')
    goods = db.session.query(Goods).filter_by(id=goodsid).first()
    print(goods)
    phone = session.get('phone')
    user = db.session.query(User).filter_by(phone=phone).first()
    addresslist = user.addresses
    return render_template('/user/order.html',goods=goods,addresses=addresslist)

