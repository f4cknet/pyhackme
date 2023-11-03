from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer,primary_key=True)
    phone = db.Column(db.String(256),nullable=False,unique=True)
    email = db.Column(db.String(100),nullable=False,unique=True)
    password = db.Column(db.String(256),nullable=False)

    def __repr__(self):
        return "(%s,%s)" %(phone,email)

class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(256),nullable=False,unique=True)
    password = db.Column(db.String(256),nullable=False)

    def __repr__(self):
        return "(%s,%s)" %(username,password)
