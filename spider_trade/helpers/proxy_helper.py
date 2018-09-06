"""
    @_how_to_use: 1. 直接另开终端运行。（但终端会阻塞） 2. 后台运行。 Unix, 后台运行脚本: <script_name> &
"""
import requests
import time
import random

# 一次获取的IP数目取决于CONCURRENT_REQUESTS和ip_pool的更新时间
PROXIES_URL = ''


def get_proxy(url=PROXIES_URL):
    """ 不构建代理池，根据url直接获取ip，缺点：多用一个HTTP请求

    :param url:
    :return:
    """
    resp = requests.get(url)
    return 'http://' + resp.text


def get_ip_pool_from_url(url=PROXIES_URL, second=5):
    """ 根据URL构造代理池，保存在文件中

    :param PROXIES_URL:
    :return: []
    """
    response = requests.get(url)
    with open('./ip_pool', 'w') as f:
        f.write(response.text)
        f.flush()
    # 每second秒构造刷新一次
    time.sleep(second)
    print('get_ip_pool is done')

def read_ip_pool_from_file(filepath='./helpers/ip_pool'):
    """ 从ip_pool文件中随机读取ip

    :return: 例如http://ip
    """
    with open(filepath, 'r') as f:
        ip_list = f.readlines()
        ip = random.choice(ip_list).strip()
        print('random ip is: ' + ip)
    print('read ip_pool is done')
    address = 'http://' + ip
    return address

if __name__ == '__main__':
    while True:
        # while True + time.sleep实现定时更新代理池文件(ip_pool)
        get_ip_pool_from_url(second=5)
        # read_ip_pool_from_file()