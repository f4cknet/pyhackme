FROM python:3.11

WORKDIR /work

COPY requirements.txt ./

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple  --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y default-mysql-client && rm -rf /var/lib/apt/lists/*

# 设置启动脚本可执行权限
COPY entrypoint.sh ./
RUN chmod +x /work/entrypoint.sh
VOLUME ["/work"]

# 启动应用
CMD ["/work/entrypoint.sh"]