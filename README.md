# vertex_renow_cookie

=======

# SH脚本
## 需要的依赖 ： jq grep sed awk

## 基本功能：通过cookie_cloud 将浏览器的cookie同步更新到vertex里面





# Python 脚本

## 需要的依赖 : configparser requests

## 基本功能：通过cookie_cloud 将浏览器的cookie同步更新到vertex里面

## 使用方法：使用仓库中的cookie_renow.py , logger.py , user_config_sample.ini,填好user_config_sample.ini的内容，改名成user_config.ini。然后开跑


# docker部署

# 下载本仓库的docker-compose.yml,user_config_sample.ini,填好user_config_sample.ini的内容，改名成user_config.ini。上面的两个文件在同一个目录里面，然后在那个目录里面敲docker-compose up -d就可以启动。（每天晚上12点同步cookies，可以选择挂载/app/log出来读取脚本的日志，也可以设置环境变量CRON_SCHEDULE改变定时时间）


## 感谢以下作者：

#### easychen / CookieCloud
#### vertex-app / vertex

