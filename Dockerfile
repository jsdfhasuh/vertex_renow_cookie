# 使用一个基础的 Alpine 镜像
FROM python:3.8-alpine

# 设置工作目录为 /app
WORKDIR /app

# 安装 cron
RUN apk --no-cache add dcron
RUN apk --no-cache add openrc

# 安装时区信息
RUN apk --no-cache add tzdata \
    && cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone

# 安装 pip
RUN apk --no-cache add python3-dev py3-pip

# 安装 requests 库
RUN pip install requests configparser PyYAML

# 添加你的 Python 脚本到容器中（如果有的话）
COPY logger.py .
COPY cookie_renow.py .
COPY setup.sh .
RUN chmod +x /app/setup.sh

# 设置定时任务环境变量，默认为每隔 24 小时
ENV CRON_SCHEDULE "0 0 */1 * *"

# 启动 SETUP 脚本，配置启动项
ENTRYPOINT ["sh", "/app/setup.sh"]