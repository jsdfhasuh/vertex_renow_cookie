#!/bin/bash


# 执行 cookie_renow.py
python /app/cookie_renow.py

# 将 cron 作业添加到 /etc/cron.d/
echo "定时时间是：$CRON_SCHEDULE"
echo "$CRON_SCHEDULE python3 /app/cookie_renow.py" > /etc/crontabs/root

# 等待一些时间确保 cron 服务已经启动
sleep 10

# 重启 cron 服务
rc-service cron restart


crond -fd