# JSDFHASUH
import requests
import json
from urllib.parse import urlparse
import yaml
import subprocess
import datetime
# import ql_api
import os
import re
import urllib.parse
from logger import *
import configparser

cookie_cloud_data={}
now = datetime.datetime.now()
formatted_datetime = now.strftime('%Y-%m-%d_%H-%M-%S')


def read_config(logger, path):
    config = configparser.ConfigParser()
    # 读取配置文件
    with open(os.path.join(path, 'user_config.ini'), 'r', encoding='utf-8') as file:
        config.read_file(file)
    return config


def has_subkey(data, key):
    """
    判断 JSON 数据中的键值是否还包含子键值

    参数:
        - data (dict): JSON 数据
        - key (str): 键名

    返回:
        - bool: 是否包含子键值
    """
    if key in data:
        # 如果键名在 JSON 数据中存在
        if isinstance(data[key], dict) and len(data[key]) > 0:
            # 如果键值是一个字典且包含子键值
            return True
    return False

def get_cookie_cloud_data():
    global cookie_cloud_data
    url = f'{cookie_cloud_host}/get/{uuid}'
    data={ 'password': cookie_password}
    response = requests.post(url, data=data)
    cookie_cloud_data=response.json()
    with open(os.path.join(BASE_DIR,f'cookie_cloud.json'),'w') as cookie_cloud_file:
        json.dump(cookie_cloud_data, cookie_cloud_file, ensure_ascii=False, indent=4)


def get_cookie(domain):
    global cookie_cloud_data
    try:
        domain_data=cookie_cloud_data['cookie_data'][domain]
    except:
        print('加前缀www和加.')
        domain = domain.replace("www.", "")
        if domain[0].lower() != ".":
            domain = '.' + domain

    try:
        domain_data = cookie_cloud_data['cookie_data'][domain]
        cookies = ';'.join([f"{obj['name']}={obj['value']}" for obj in domain_data])
        #print(cookies)
        return cookies
    except Exception as e:
        print(f'发生{e}错误，找不到站点{domain}的cookies')
        return None
    #print(cookie_cloud_data)



def get_vertex_cookie():
    url = f'{vertex_host}/api/user/login'
    data = {'username': username, 'password': password}
    session = requests.Session()
    response = session.post(url, data=data)
    print(response.text)
    # 获取cookie
    cookies = session.cookies.get_dict()
    print(cookies)
    cookies='; '.join([f'{key}={value}' for key, value in cookies.items()])

    return cookies

def renow_vertex_douban(douban_cookie):
    url = f'{vertex_host}/api/subscribe/list'
    url_modify = f'{vertex_host}/api/subscribe/modify'
    headers = {
        "Cookie": f"{get_vertex_cookie()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data=response.json()['data']
    for element in data:
        print(f"{element['alias']}更新豆瓣cookies")
        element['cookie']=douban_cookie
        json_data = json.dumps(element)
        response = requests.post(url_modify, data=json_data,headers=headers)
        print(response.text)


def renow_vertex_site():
    url = f'{vertex_host}/api/site/list'
    url_modify = f'{vertex_host}/api/site/modify'
    headers = {
        "Cookie": f"{get_vertex_cookie()}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    data = response.json()['data']['siteList']

    for site in data:
        parsed_url = urlparse(site['index'])
        # 提取出域名信息
        domain = parsed_url.netloc
        if get_cookie(domain) != None:
            site['cookie']=get_cookie(domain)
        json_data = json.dumps(site)
        response = requests.post(url_modify, data=json_data,headers=headers)
        print(response.text)

def renow_flexget(config_path,site_folder):
    file=config_path
    with open(file, 'r', encoding='utf-8') as start_file:
        flexget_data = yaml.load(start_file,Loader=yaml.FullLoader)
    sites=flexget_data['variables']['sites']
    for site in sites:
        with open(os.path.join(site_folder,f'{site}.py'),'r',encoding='utf-8') as sitepy:
            raw_content = sitepy.read()
            # 使用正则表达式提取URL
            match = re.search(r"URL:\s*Final\s*=\s*'([^']+)'", raw_content)
            if match:
                url = match.group(1)
                print(url)
        parsed_url = urllib.parse.urlparse(url)
        domain = parsed_url.netloc
        print(f'站点名：{domain}')
        cookie = get_cookie(domain) #
        if cookie:
            if has_subkey(sites, site):
                sites[site]['cookie']=get_cookie(domain)
            else:
                sites[site] = cookie
    with open(file, 'w') as result:
        yaml.dump(flexget_data, result)

def back_up_vertex(file_path):
    url = f'{vertex_host}/api/setting/backupVertex'
    headers = {
        "Cookie": f"{get_vertex_cookie()}",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # 提取文件名

        file_name = 'Vertex-backups-'+formatted_datetime+'.tar.gz'  # 假设下载链接的文件名在最后一个斜杠后面
        file_name = os.path.join(file_path,file_name)
        # 保存文件
        with open(file_name, 'wb') as file:
            file.write(response.content)
        print('文件下载成功:', file_name)
    else:
        print('文件下载失败，HTTP状态码:', response.status_code)

def split_cookie(cookie):
    # 去掉字符串中的空格
    cookies_dict={}
    cookies_str = cookie.replace(" ", "")

    # 按分号分割字符串
    cookies_list = cookies_str.split(";")

    # 分割键值对并存入字典
    for cookie in cookies_list:
        key_value = cookie.split("=", 1)
        if len(key_value) == 2:
            key = key_value[0]
            value = key_value[1]
            cookies_dict[key] = value
    return cookies_dict

def cookie_add(main,second):
    second=split_cookie(second)
    for element in second:
        if element in main:
            continue
        else:
            main += f";{element}:{second[element]}"
    return main
    pass

def write_dict_to_json(data, filename):
    with open(filename, "w") as json_file:
        json.dump(data, json_file, ensure_ascii=False,indent=4)
    print(f"字典已写入 JSON 文件: {filename}")

def read_dict_from_json(filename):
    with open(filename, "r") as json_file:
        loaded_data = json.load(json_file)
    return loaded_data

if __name__=='__main__':
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    logger = get_logger(name=f'cookie_renow', path=BASE_DIR, func_name='main')
    config = read_config(logger=logger, path=os.path.dirname(os.path.abspath(__file__)))
    if not config.has_section(section='Vertex'):
        logger.info('没有填入Vertex信息，小哥哥')
        exit(0)
    else:
        logger.info('开始读取Vertex信息')
        vertex_host= config.get('Vertex', 'host')    ###填入vertex的地址
        password= config.get('Vertex', 'password')    ###填入vertex的密码，通过f12获取  或者自己原来的密码 md5加密32位 小写
        username= config.get('Vertex', 'username')   ###填入vertex的用户名
        file_path = config.get('Vertex', 'back_up_path')   # Vertex备份路径                 
    if not config.has_section(section='Cookie_cloud'):
        logger.info('没有填入Cookie_cloud信息，小哥哥')
        exit(0)
    else:
        logger.info('开始读取Cookie_cloud信息')
        cookie_cloud_host=config.get('Cookie_cloud', 'host') ###填入cookie_cloud的地址
        cookie_password=config.get('Cookie_cloud', 'password')     ###填入cookie_cloud的密码
        uuid=config.get('Cookie_cloud', 'uuid')                 ###填入cookie_cloud的用户名
    if not config.has_section(section='Flexget'):
        logger.info('没有填入Flexget信息，小哥哥')
        
    else:
        logger.info('开始读取Flexget信息')
        container_name=config.get('Flexget', 'container_name') ###填入cookie_cloud的地址
        config_path=config.get('Flexget', 'config_path') ###填入cookie_cloud的地址
        site_folder=config.get('Flexget', 'site_folder') ###填入cookie_cloud的地址

    if file_path:
        logger.info('开始备份Vertex到{file_path}')
        back_up_vertex(file_path=file_path)  # 备份vertex,传入路径就备份
    save_data_json = os.path.join(BASE_DIR,'save_data.json')
    if not os.path.exists(path=save_data_json):
        logger.info('创建sava_data_json')
        empty_data = {}
        with open(save_data_json, 'w') as json_file:
            json.dump(empty_data, json_file)
    
    save_data=read_dict_from_json(filename=save_data_json)
    get_cookie_cloud_data()
    douban_cookie=get_cookie('.douban.com')
    moive_cookie=get_cookie('.movie.douban.com')
    """
    bilibili_cookie=get_cookie('.www.bilibili.com')
    ql_token=ql_api.ql_login('Vt_tztUiE4oO','iUQNhsZt7f___a9emb67c4_3')
    ql_api.renow_env(ql_token,19,bilibili_cookie,'Ray_BiliBiliCookies__0','jsdfhasuh')
    """
    all_douban_cookie=cookie_add(main=douban_cookie,second=moive_cookie)
    
    ck_value = re.search(r'ck=([^;]+)', all_douban_cookie)
    # Check if the match is found
    if ck_value:
        ck_value = ck_value.group(1)
        save_data['ck'] = ck_value
        logger.info(f'The value of ck is: {ck_value}')
        write_dict_to_json(data=save_data,filename=save_data_json)
    elif 'ck' in save_data:
        name = 'ck'
        value = save_data[name]
        all_douban_cookie += f';{name}={value};'
        logger.info(f'No match found for ck,douban:{all_douban_cookie}')
    else:
        logger.info('save_data 没有ck值，请登录豆瓣同步')

    logger.info(f'all_douban_cookie:{all_douban_cookie}')
    renow_vertex_douban(all_douban_cookie)
    renow_vertex_site()

    if config.has_section(section='Flexget'):      
        renow_flexget(config_path=config_path,site_folder=site_folder)
        subprocess.run(["docker", "restart", container_name])