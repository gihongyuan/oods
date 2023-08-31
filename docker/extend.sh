#!/bin/bash

# 读取环境变量
if [ -n "$FILE_CACHE_TIME" ]; then
    CACHE_TIME="$FILE_CACHE_TIME"
else
    CACHE_TIME=86400
fi

if [ -n "$HTTP_OODS_PORT" ]; then
    HTTP_OODS_PORT="$HTTP_OODS_PORT"
else
    HTTP_OODS_PORT=9080
fi

if [ -n "$HTTPS_OODS_PORT" ]; then
    HTTPS_OODS_PORT="$HTTPS_OODS_PORT"
else
    HTTPS_OODS_PORT=9443
fi

# 更新文件大小限制（200M）
sed -i -e 's/104857600/209715200/g' /etc/onlyoffice/documentserver-example/production-linux.json
sed -i -e 's/104857600/209715200/g' /etc/onlyoffice/documentserver/default.json
sed -i -e 's/50MB/200MB/g' /etc/onlyoffice/documentserver/default.json
sed -i 's/^client_max_body_size 100m;$/client_max_body_size 200m;/' /etc/onlyoffice/documentserver/nginx/includes/ds-common.conf

# 新增自有服务启动配置
cp -f /etc/supervisor/conf.d/oods.conf.example /etc/supervisor/conf.d/oods.conf
sed -i "s/9080/${HTTP_OODS_PORT}/g" /etc/supervisor/conf.d/oods.conf
sed -i "s/9443/${HTTPS_OODS_PORT}/g" /etc/supervisor/conf.d/oods.conf

# 更新缓存过期配置
sed -i "/CoAuthoring/a \\
      \"expire\": { \\
        \"files\": ${CACHE_TIME}, \\
        \"filesCron\": \"*/10 * * * * *\" \\
      }," /etc/onlyoffice/documentserver/local.json

# 更新https配置
#openssl genrsa -out onlyoffice.key 2048
#openssl req -new -key onlyoffice.key -out onlyoffice.csr
#openssl x509 -req -days 3650 -in onlyoffice.csr -signkey onlyoffice.key -out onlyoffice.crt
mkdir -p /app/onlyoffice/DocumentServer/data/certs
cp /app/certs/onlyoffice.crt /app/onlyoffice/DocumentServer/data/certs/
cp /app/certs/onlyoffice.key /app/onlyoffice/DocumentServer/data/certs/
chmod 400 /app/onlyoffice/DocumentServer/data/certs/onlyoffice.key

# 服务重启
service nginx restart
supervisorctl reread
supervisorctl update
supervisorctl restart ds:docservice
supervisorctl restart ds:converter
supervisorctl restart ds:metrics