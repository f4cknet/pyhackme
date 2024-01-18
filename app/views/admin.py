# -*-utf-8-*-
import oss2,io
from flask import Blueprint,request,render_template,session,redirect
from app.models import Admin,db,Goods
from app.common.argon2hash import argon2hasher
from app.common.authen import valid_admin,redis_client,protect_user_login,is_login
from uuid import  uuid4
from app import config
import urllib


adminapp = Blueprint('admin',__name__,url_prefix='/admin')

@adminapp.route('/register',methods=["GET","POST"])
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


@adminapp.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        result = valid_admin(username,password)
        if result is True:
            session['username'] = username
            return "恭喜你，登陆成功"
        else:
            return "登录失败"

    return render_template('admin/login.html')

@adminapp.route('/add_admin',methods=['GET','POST'])
@is_login
def add_admin():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        password_hash = argon2hasher(password)
        commit_csrf_token = request.form.get('csrf_token')
        if commit_csrf_token == redis_client.get(session['username']).decode('utf-8'):
            admin = Admin(username=username, password=password_hash)
            db.session.add(admin)
            db.session.commit()
            return "添加用户成功"
        else:
            return "CSRF TOKNE校验失败，无法添加用户"

    username = session['username']
    csrf_token = str(uuid4())
    redis_client.setex(username,600,csrf_token)
    return render_template('admin/add_admin.html',csrf_token=csrf_token)


@adminapp.route('/home',methods=['GET'])
@is_login
def home():
    return render_template('admin/home.html')


@adminapp.route('/admin_list',methods=['GET'])
@is_login
def admin_list():
    admin_list = db.session.query(Admin).all()
    return render_template('admin/admin_list.html',admin_list=admin_list)

@adminapp.route('/add_goods',methods=['POST','GET'])
@is_login
def add_goods():
    if request.method == "POST":
        goodsname = request.form.get('goodsname')
        category = request.form.get('category')
        mainimg = request.form.get('mainimg')
        content = request.form.get('content')
        sku = request.form.get('sku')
        price = request.form.get('price')

        try:
            db.session.add(Goods(goodsname=goodsname,category=category,mainimg=mainimg,content=content,sku=sku,price=price))
            db.session.commit()
            return "成功添加商品"
        except Exception as e:
            return "添加商品失败" + str(e)
    return render_template('admin/goods_add.html')

@adminapp.route('/goods_list',methods=['GET'])
@is_login
def goods_list():
    goods_list = db.session.query(Goods).all()
    return render_template('admin/goods_list.html',goods_list=goods_list)

@adminapp.route('/batch_goods',methods=['GET','POST'])
@is_login
def batch_goods():
    if request.method == "POST":
        batchfile = request.form.get('batchfile')

        print(urllib.request.urlopen(batchfile).read())
        goods_lists = urllib.request.urlopen(batchfile).read().decode('utf-8') #ssrf
        # goods_lists = requests.get(batchfile).content.decode('utf-8')
        try:
            content = goods_lists.split('\r\n')
            num = len(content)
            for i in range(1,num+1):
                if i<num+1:
                    items = content[i].split(',')
                    for row in items:
                        goods = Goods(
                            goodsname=row[0],
                            category=row[1],
                            mainimg=row[2],
                            content=row[3],
                            sku=int(row[4]),
                            price=float(row[5])
                        )

                        db.session.add(goods)
            db.session.commit()
            return content
        except:
            return content
    return render_template('admin/batch_goods.html')

@adminapp.route('/upload_goodsfile',methods=['POST'])
@is_login
def upload_goodsfile():
    ak = config.ossak
    sk = config.osssk
    auth = oss2.Auth(ak,sk)
    endpoint = "https://oss-cn-beijing.aliyuncs.com"
    bucket = oss2.Bucket(auth,endpoint,'m1nzhi')
    upload_file = request.files.get('file')
    upload_file_name = str(uuid4())+'.csv'
    upload_result = bucket.put_object(upload_file_name,upload_file)
    if upload_result.status == 200:
        file_url = bucket.sign_url('GET',upload_file_name,600)
        print(file_url)
        return {"fileUrl":file_url}
    else:
        return {"code":400,"msg":"上传失败"}

