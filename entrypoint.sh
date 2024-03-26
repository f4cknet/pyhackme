#!/bin/bash

# 确保数据库存在
flask db init

# 创建数据库迁移脚本
flask db migrate

# 应用数据库迁移
flask db upgrade

# 启动 Flask 应用
flask run --host=0.0.0.0 --debug