#!/bin/bash


# 执行 cookie_renow.py
python /app/cookie_renow.py

# 将 cron 作业添加到 /etc/cron.d/
echo "定时时间是：$CRON_SCHEDULE"
echo "$CRON_SCHEDULE root python3 /app/cookie_renow.py" > /etc/crontabs/root

# 等待一些时间确保 cron 服务已经启动
sleep 10

# 重启 cron 服务
rc-service cron restart


# 无限循环以保持脚本执行
while true
do
    # 执行其他操作，如果有的话
    # ...

    # 等待一段时间，以免脚本过于频繁运行
    sleep 3600  # 例如，等待1小时
done