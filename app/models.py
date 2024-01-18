from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_goods = db.Table('user_goods',
                      db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
                      db.Column('goods_id',db.Integer,db.ForeignKey('goods.id'))
                      )

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    phone = db.Column(db.String(256),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(256),nullable=False)
    balance = db.Column(db.Float)
    goods = db.relationship('Goods',secondary=user_goods,back_populates='users')
    orders = db.relationship('Order',backref='user')
    addresses = db.relationship('Address',backref='user')

    def __repr__(self):
        return "(%s,%s)" %(self.phone,self.email)

class Address(db.Model):
    __tablename__ = "address"
    id = db.Column(db.Integer,primary_key=True)
    receiver = db.Column(db.String(16),nullable=False)
    phone = db.Column(db.String(256),nullable=False)
    addressname = db.Column(db.String(256))
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    orders = db.relationship('Order',backref='address')


    def __repr__(self):
        return "(%s,%s,%s)" %(self.receiver,self.addressname,self.user_id)


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(256),nullable=False,unique=True)
    password = db.Column(db.String(256),nullable=False)

    def __repr__(self):
        return "(%s,%s)" %(self.username,self.password)

class Goods(db.Model):
    __tablename__ = "goods"
    id = db.Column(db.Integer,primary_key=True)
    goodsname = db.Column(db.String(256),nullable=False)
    category = db.Column(db.String(256),nullable=False)
    mainimg = db.Column(db.String(1024),nullable=False)
    content = db.Column(db.Text,nullable=False)
    sku = db.Column(db.Integer,nullable=False)
    price = db.Column(db.Float,nullable=False)
    users = db.relationship('User', secondary=user_goods, back_populates='goods')
    orders = db.relationship('Order',back_populates='goods')

    def __repr__(self):
        return "(%s,%s,%s,%d,%f)" %(self.goodsname,self.mainimg,self.category,self.price,self.sku)

class Order(db.Model):
    __tablename__ = "order"
    id = db.Column(db.String(32),primary_key=True,unique=True)
    generatetime = db.Column(db.DateTime)
    status = db.Column(db.String(1),default="0")
    payment_method = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    goods_id = db.Column(db.Integer, db.ForeignKey('goods.id'))
    address_id = db.Column(db.Integer,db.ForeignKey('address.id'))
    goods = db.relationship('Goods',back_populates='orders')

    def __repr__(self):
        return "(%s,%s,%s,%s)" %(self.generatetime,self.status,self.user_id,self.goods_id)




