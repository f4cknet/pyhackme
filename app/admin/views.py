from flask import Blueprint,request,render_template
from app.models import Admin,db
from app.common.argon2hash import argon2hasher
from app.common.authen import valid_admin,redis_client,protect_user_login


admin = Blueprint('admin',__name__,url_prefix='/admin')

@admin.route('/register',methods=["GET","POST"])
def register():
    if request.method == "POST":
        #注册逻辑
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            return '两次密码不一致，重新注册'
        try:
            password_hash = argon2hasher(password)
            admin = Admin(username=username, password=password_hash)
            db.session.add(admin)
            db.session.commit()
            return "注册成功"
        except Exception as e:
            return "已存在该用户"
            db.session.rollback()
            raise e
        else:
            return "两次密码不一致，重新注册"

    return render_template("/admin/register.html")

@admin.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        result = valid_admin(username,password)
        if result is True:
            return "恭喜你，登陆成功"
        else:
            return "登录失败"

    return render_template('admin/login.html')
