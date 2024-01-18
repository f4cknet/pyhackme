from flask import Blueprint,session,request,jsonify,render_template
from app.models import User,db,Goods,Order
from app.common.authen import user_is_login
from uuid import uuid4
from datetime import datetime
from app.common.lib import query_order


orderapp = Blueprint('order',__name__,url_prefix='/order')

@orderapp.route('/',methods=['GET','POST'])
@user_is_login
def index():
    user_id = session.get('user_id')
    if request.method == "POST":
        data = request.json
        addressid = data.get('address')
        goodsid = data.get('goods')
        randomuid = str(uuid4())
        randomuid_list = randomuid.split('-')
        order_id = ''.join(randomuid_list)
        generatetime = datetime.now()
        order = Order(id=order_id,generatetime=generatetime,user_id=user_id,goods_id=goodsid,payment_method="",address_id=addressid)
        try:
            db.session.add(order)
            db.session.commit()
            return jsonify({"code":201,"order_id":order_id})
        except:
            return jsonify({"code":501,"msg":"error"})

    goodsid = request.args.get('goodsid')
    goods = db.session.query(Goods).filter_by(id=goodsid).first()
    print(goods)
    user = db.session.query(User).filter_by(id=user_id).first()
    addresslist = user.addresses
    return render_template('/user/order.html',goods=goods,addresses=addresslist)


@orderapp.route('/list',methods=["GET","POST"])
@user_is_login
def orderlist():
    orders = Order.query.filter_by(user_id=session.get('user_id')).all()
    orderinfos = [{"goods":order.goods.goodsname,"price":order.goods.price,"orderid":order.id,"orderstatus":order.status,"time":order.generatetime} for order in orders]
    return render_template("/user/orderlist.html",orders=orderinfos)


@orderapp.route('/detail',methods=["GET"])
@user_is_login
def orderdetail():
    if request.args.get('orderid'):
        orderid = request.args.get('orderid')
        data = query_order(orderid)
        orderinfo = data[0]
        if orderinfo:
            order = {
                "orderid":orderinfo[0],
                "generatetime":orderinfo[1],
                "orderstatus":orderinfo[2],
                "payment":orderinfo[3],
                "receiver":orderinfo[4],
                "goodsname":orderinfo[5],
                "phone":orderinfo[6],
                "addressname":orderinfo[7]
            }
            return render_template("/user/orderdetail.html",order=order)
        else:
            return render_template('/user/orderdetail.html')
    else:
        return "参数错误"

@orderapp.route('/refund/<order_id>',methods=['GET','POST'])
@user_is_login
def refund(order_id):
    try:
        order = Order.query.get(order_id)
        if order.status != str(3):
            order.status = str(3)
            db.session.commit()
            return jsonify({"code":200,"msg":"成功发起退款"})
        return jsonify({"code":500,"msg":"已在退款中，等待商家确认退款"})
    except:
        db.session.rollback()
        return "退款失败"

@orderapp.route('/payment/<order_id>',methods=['GET','POST'])
@user_is_login
def payment(order_id):
    order = Order.query.get(order_id)
    user = User.query.filter_by(id=order.user_id).first()
    goods = Goods.query.get(order.goods_id)
    if request.method == "POST":
        payment_method = request.form.get('payment_method')
        balance = user.balance
       # goodsid = order.goods_id
        order.payment_method = payment_method
        if payment_method == "balance":
            if balance < goods.price:
                return "余额不足"
            user.balance = balance - goods.price
            order.status = "1"
            goods.sku = goods.sku-1
            db.session.commit()
            return "支付成功！订单ID: {}".format(order_id)
        else:
            return "暂不支持该方式支付"
    if order:
        return render_template("/user/payment.html",order=order,user=user,goods=goods)
    else:
        return "订单不存在"