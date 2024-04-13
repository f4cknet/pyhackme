#!/bin/bash

until mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

if [ ! -f "migrations" ]; then
    flask db init
fi

# 等待 MySQL 服务启动
until mysqladmin ping -h"$MYSQL_HOST" -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" --silent; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

# 检查是否有数据库变更
FLASK_DB_STATUS=$(flask db stamp head)
if [ "$FLASK_DB_STATUS" != "Already at revision 'head'" ]; then
    flask db migrate
    flask db upgrade
fi

# 启动 Flask 应用
flask run --host=0.0.0.0 --debug