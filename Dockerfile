FROM onlyoffice/documentserver:7.3.0

# 安装pip
RUN apt-get update && apt-get install -y --no-install-recommends python3-pip && rm -rf /var/lib/apt/lists/*

# pip换源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple && pip config set install.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装依赖
COPY requirements.txt /app/requirements.txt
RUN cd /app && pip install --no-cache-dir -r requirements.txt && rm -rf ~/.cache/pip

# 拷贝项目代码
COPY oods /app/oods

# 拷贝证书
COPY ./docker/certs /app/certs

# 修改启动配置
COPY ./docker/nginx/ds-oods.conf /etc/nginx/includes/ds-00ds.conf
COPY ./docker/nginx/https.conf /etc/nginx/conf.d
COPY ./docker/supervisor/oods.conf /etc/supervisor/conf.d/oods.conf.example
COPY ./docker/extend.sh /app/extend.sh
RUN sed -i '/tail -f \/var\/log\//i sh /app/extend.sh' /app/ds/run-document-server.sh




