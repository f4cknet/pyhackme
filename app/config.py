import os
ossak = os.environ.get('ossak')
osssk = os.environ.get('osssk')

mysql_user =  os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_host = os.environ.get('MYSQL_HOST')
mysql_database = os.environ.get('MYSQL_DATABASE')

redis_host = os.environ.get('REDIS_HOST')
redis_password = os.environ.get('REDIS_PASSWORD')



SQLALCHEMY_DATABASE_URI = f"mysql://{mysql_user}:{mysql_password}@{mysql_host}:3306/{mysql_database}?charset=utf8"
SECRET_KEY = "hackmemdakldmsakl"

MAIL_SERVER = os.environ.get('MAIL_SERVER')
MAIL_PORT = os.environ.get('MAIL_PORT')
MAIL_USE_SSL = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')