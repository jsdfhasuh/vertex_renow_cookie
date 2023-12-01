#!/bin/bash

####

    vertex_host="http://192.168.1.128:3000"    ###填入vertex的地址
	cookie_cloud_host="http://192.168.1.125:8088/cookie"  ###填入cookie_cloud的地址
	cookie_password="csASVX41KUHa49pguigyvM"      ###填入cookie_cloud的密码
	password="95f0f96bc5836c39387a66c1ba766367"   ###填入vertex的密码，通过f12获取  或者自己原来的密码 md5加密32位 小写
	username="admin"                              ###填入vertex的用户名
####	
	
	#!/bin/bash

####

    vertex_host="http://192.168.1.128:3000"    ###填入vertex的地址
	cookie_cloud_host="http://192.168.1.125:8088/cookie"  ###填入cookie_cloud的地址
	cookie_password="jVStfJnWgamcymoxUJ1hS4"      ###填入cookie_cloud的密码
	uuid="csASVX41KUHa49pguigyvM"                 ###填入cookie_cloud的用户名
	password="95f0f96bc5836c39387a66c1ba766367"   ###填入vertex的密码，通过f12获取  或者自己原来的密码 md5加密32位 小写
	username="admin"                              ###填入vertex的用户名
####	
	
	
	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	DIR_past="$(echo "$DIR" | grep -oP "/.*/"|sed -r "s#(/$)##g")"
	echo $DIR
	echo $DIR_past
	log=$DIR/cookie_renow.log
	cookie=$DIR/cookie.json
	site=$DIR/site.json
	subscribe=$DIR/subscribe.json
	set -x
	echo "$(curl -X POST  -d "password=$cookie_password" "$cookie_cloud_host/get/$uuid"| jq '.cookie_data')" > $cookie
    vertex_cookie="$(curl -i --header 'Referer: '$vertex_host'' --data 'username='$username'&password='$password'' "$vertex_host/api/user/login" | grep -Eo "Set.Cookie.*"|sed -r "s#Set.Cookie: ##g"|sed -r "s#\r##g")"
	echo $vertex_cookie
    exec >$log 2>&1
   
get_cookie()
{	
    final_cookie=""
	domain=$1
	echo $domain
	element="$(cat $cookie | jq '."'$domain'"')"
	time="$(echo $element | awk -v RS='domain' 'END {print --NR}' )"
	final_cookie=""
	for i in $(seq 1 $time)
		do
		element_name="$(echo $element | jq '.['$(($i-1))'].name'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		element_value="$(echo $element | jq '.['$(($i-1))'].value'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo "$element_name""=""$element_value"
		final_cookie="$final_cookie""$element_name""=""$element_value"";"
		done
	final_cookie="$(echo $final_cookie|sed -r "s#;\$##g"|sed -r "s#\r##g")"
	echo $final_cookie
}

renow_site()
{
	echo "$(curl --cookie "$vertex_cookie" -H "Content-Type: application/json" "$vertex_host/api/site/list"|jq '.data.siteList')" > $site
	time="$(cat $site | grep -c "cookie")"
	mkdir -p $DIR/allsite
	for i in $(seq 1 $time)
		do
		
		vertex_name="$(cat $site | jq '.['$(($i-1))'].name'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo  "$(cat $site|jq '.['$(($i-1))']')" > $DIR/allsite/"$vertex_name".json
		vertex_site="$(cat $site | jq '.['$(($i-1))'].index'| sed -r "s#\"##g"|sed -r "s#[\]##g"|awk  'BEGIN {FS="/"} {print $3}')"
		get_cookie "$vertex_site"
		echo "$(cat $DIR/allsite/"$vertex_name".json | jq --arg v $final_cookie  '.cookie=$v')" > $DIR/allsite/"$vertex_name".json
		curl -X POST --cookie "$vertex_cookie" -H "Content-Type: application/json" --data @"$DIR/allsite/"$vertex_name".json" "$vertex_host/api/site/modify"
		sleep 5
		done
}

renow_douban()
{
	echo "$(curl --cookie "$vertex_cookie" -H "Content-Type: application/json" "$vertex_host/api/subscribe/list"|jq '.data')" > $subscribe
	time="$(cat $subscribe | grep -c "categories")" 
	mkdir -p $DIR/allsubscribe
	for i in $(seq 1 $time)
		do		
		vertex_name="$(cat $subscribe | jq '.['$(($i-1))'].alias'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo  "$(cat $subscribe|jq '.['$(($i-1))']')" > $DIR/allsubscribe/"$vertex_name".json
		get_cookie ".douban.com"
		echo "$(cat $DIR/allsubscribe/"$vertex_name".json | jq --arg v $final_cookie  '.cookie=$v')" > $DIR/allsubscribe/"$vertex_name".json
		curl -X POST --cookie "$vertex_cookie" -H "Content-Type: application/json" --data @"$DIR/allsubscribe/"$vertex_name".json" "$vertex_host/api/subscribe/modify"
		sleep 5
		done
}

	renow_douban
	renow_site
set +x

	DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
	DIR_past="$(echo "$DIR" | grep -oP "/.*/"|sed -r "s#(/$)##g")"
	echo $DIR
	echo $DIR_past
	log=$DIR/cookie_renow.log
	cookie=$DIR/cookie.json
	site=$DIR/site.json
	subscribe=$DIR/subscribe.json
	set -x
	echo "$(curl -X POST  -d "password=$cookie_password" "$cookie_cloud_host/get"|jq '.cookie_data')" > $cookie
    vertex_cookie="$(curl -i --header 'Referer: '$vertex_host'' --data 'username='$username'&password='$password'' "$vertex_host/api/user/login" | grep -Eo "Set.Cookie.*"|sed -r "s#Set.Cookie: ##g"|sed -r "s#\r##g")"
	echo $vertex_cookie
    exec >$log 2>&1
   
get_cookie()
{	
    final_cookie=""
	domain=$1
	echo $domain
	element="$(cat cookie.json | jq '."'$domain'"')"
	time="$(echo $element | awk -v RS='domain' 'END {print --NR}' )"
	final_cookie=""
	for i in $(seq 1 $time)
		do
		element_name="$(echo $element | jq '.['$(($i-1))'].name'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		element_value="$(echo $element | jq '.['$(($i-1))'].value'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo "$element_name""=""$element_value"
		final_cookie="$final_cookie""$element_name""=""$element_value"";"
		done
	final_cookie="$(echo $final_cookie|sed -r "s#;\$##g"|sed -r "s#\r##g")"
	echo $final_cookie
}

renow_site()
{
	echo "$(curl --cookie "$vertex_cookie" -H "Content-Type: application/json" "$vertex_host/api/site/list"|jq '.data.siteList')" > $site
	time="$(cat $site | grep -c "cookie")"
	mkdir -p $DIR/allsite
	for i in $(seq 1 $time)
		do
		
		vertex_name="$(cat $site | jq '.['$(($i-1))'].name'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo  "$(cat $site|jq '.['$(($i-1))']')" > $DIR/allsite/"$vertex_name".json
		vertex_site="$(cat $site | jq '.['$(($i-1))'].index'| sed -r "s#\"##g"|sed -r "s#[\]##g"|awk  'BEGIN {FS="/"} {print $3}')"
		get_cookie "$vertex_site"
		echo "$(cat $DIR/allsite/"$vertex_name".json | jq --arg v $final_cookie  '.cookie=$v')" > $DIR/allsite/"$vertex_name".json
		curl -X POST --cookie "$vertex_cookie" -H "Content-Type: application/json" --data @"$DIR/allsite/"$vertex_name".json" "$vertex_host/api/site/modify"
		sleep 5
		done
}

renow_douban()
{
	echo "$(curl --cookie "$vertex_cookie" -H "Content-Type: application/json" "$vertex_host/api/subscribe/list"|jq '.data')" > $subscribe
	time="$(cat $subscribe | grep -c "categories")" 
	mkdir -p $DIR/allsubscribe
	for i in $(seq 1 $time)
		do		
		vertex_name="$(cat $subscribe | jq '.['$(($i-1))'].alias'| sed -r "s#\"##g"|sed -r "s#[\]##g")"
		echo  "$(cat $subscribe|jq '.['$(($i-1))']')" > $DIR/allsubscribe/"$vertex_name".json
		get_cookie ".douban.com"
		echo "$(cat $DIR/allsubscribe/"$vertex_name".json | jq --arg v $final_cookie  '.cookie=$v')" > $DIR/allsubscribe/"$vertex_name".json
		curl -X POST --cookie "$vertex_cookie" -H "Content-Type: application/json" --data @"$DIR/allsubscribe/"$vertex_name".json" "$vertex_host/api/subscribe/modify"
		sleep 5
		done
}

	renow_douban
	renow_site
set +x
