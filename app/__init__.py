from flask import Flask
from app.user.views import user
from app.admin.views import admin
from app.models import db
from flask_migrate import  Migrate
import pymysql
pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder="../templates",static_folder="../static")
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://hackme:admin123456@localhost:3306/hackme"
app.register_blueprint(user)
app.register_blueprint(admin)
db.init_app(app)
migrate = Migrate(app,db)



if __name__ == '__main__':
    app.run(debug=True)
