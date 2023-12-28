from flask import Flask
from app.user.views import user
from app.admin.views import admin
from app.models import db
from flask_migrate import Migrate
import pymysql
from flask_mail import Mail
pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder="../templates",static_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://hackme:Hackme123!@localhost:3306/hackme?charset=utf8"
app.config['SECRET_KEY'] = "hackmemdakldmsakl"
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'zmzsg100@163.com'
app.config['MAIL_PASSWORD'] = 'FZVDQWVEXOPNQQHP'
app.config['MAIL_DEFAULT_SENDER'] = 'zmzsg100@163.com'


app.register_blueprint(user)
app.register_blueprint(admin)
db.init_app(app)
mail = Mail(app)


migrate = Migrate(app,db)



if __name__ == '__main__':
    app.run(debug=True)
