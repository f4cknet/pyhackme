from flask import Flask,render_template
from app.views.user import userapp
from app.views.admin import adminapp
from app.views.order import orderapp
from app.models import db,Goods
from flask_migrate import Migrate
from app import config
import pymysql
from flask_mail import Mail
pymysql.install_as_MySQLdb()

app = Flask(__name__,template_folder="../templates",static_folder="../static")
app.config.from_pyfile('config.py')


app.register_blueprint(userapp)
app.register_blueprint(adminapp)
app.register_blueprint(orderapp)
db.init_app(app)
mail = Mail(app)

@app.route('/',methods=['GET'])
def shoplist():
    goods_lists = db.session.query(Goods).all()
    return render_template('/user/goods_lists.html',goods_lists=goods_lists)



migrate = Migrate(app,db)



if __name__ == '__main__':
    app.run(debug=True)
