# 提取版本
version=$(cat VERSION)
docker build -t oods:"${version}" .