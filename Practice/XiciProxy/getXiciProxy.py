import requests
import re
import time
import random
import redis

headers_keys = [
    'Mozilla/5.0 (Linux; Android 4.1.1; Nexus 7 Build/JRO03D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Safari/535.19',
    'Mozilla/5.0 (Linux; U; Android 4.0.4; en-gb; GT-I9300 Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    'Mozilla/5.0 (Linux; U; Android 2.2; en-gb; GT-P1000 Build/FROYO) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
    'Mozilla/5.0 (Android; Mobile; rv:14.0) Gecko/14.0 Firefox/14.0',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36',
    'Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19',
    'Mozilla/5.0 (iPad; CPU OS 5_0 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko) Version/5.1 Mobile/9A334 Safari/7534.48.3',
    'Mozilla/5.0 (iPod; U; CPU like Mac OS X; en) AppleWebKit/420.1 (KHTML, like Gecko) Version/3.0 Mobile/3A101a Safari/419.3'
]

redis_key = 0

# 批量获取高匿代理ip
def getXCProxyIp(max_page_number):
    for i in range(1, max_page_number + 1):
        # 伪装浏览器 headers
        headers = {
            'User-Agent': headers_keys[random.randint(0, len(headers_keys) - 1)]
        }
        page_number = i
        init_url = 'http://www.xicidaili.com/wt/' + str(i)
		# 增加重连次数
		requests.adapters.DEFAULT_RETRIES = 5
		s = requests.session()
		# 关闭多余连接
		s.keep_alive = False 
        req = s.get(init_url, headers=headers)
        # 获取代理 ip
        agency_ip_re = re.compile(r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b' ,re.S)
        agency_ip = agency_ip_re.findall(req.text)
        # 获取代理 ip 的端口号
        agency_port_re = re.compile('<td>([0-9]{2,5})</td>', re.S)
        agency_port = agency_port_re.findall(req.text)
        # 高匿代理 ip 页面中所列出的 ip 数量
        ip_number = len(agency_ip)
        print('getting page %d （please wating）......' % page_number)
        for i in range(ip_number):
            total_ip = agency_ip[i] + ':' + agency_port[i]
            print(total_ip)
            verifyProxyIP(agency_ip[i], agency_port[i])
            time.sleep(1)
        print('the %d pages is OK' % page_number)
        print('------------------------------------')
        time.sleep(2)

# 验证获取到的代理IP是否可用
def verifyProxyIP(verify_ip, verify_ip_port):
    print('verifying this Proxy IP......')
    try:
        # 设置测 ip 的地址
        url = "http://2018.ip138.com/ic.asp"
        proxies = {
          "http": "http://"+verify_ip+':'+verify_ip_port,
        }
        response = requests.get(url, proxies=proxies,timeout=5)
    except :
        print(verify_ip+' xxxxxxxxxxxxxxxxxxxx is not OK') 
    else:
        curIP = re.findall(r'\d+\.\d+\.\d+\.\d+',response.text,re.S)
        if len(curIP) > 0 and curIP[0] == verify_ip:
            print(verify_ip+' ^^^^^^^^^^^^^^^^^^^ is OK')
            available_ip = verify_ip + ':' + verify_ip_port
            saveProxyIP(available_ip,redis_r)
        else:
            print(verify_ip+' xxxxxxxxxxxxxxxxxxxx is not OK') 
    print('\n')
        

# 将可用的代理IP保存到 Redis
def saveProxyIP(available_ip,redis):
    global redis_key
    if redis.set('ip'+str(redis_key),available_ip):
        redis_key+=1
    else:
        print('saveProxyIP error')

if __name__ == '__main__':
    print('----------get  http ip  ----------')
    page= int(input('pleae input how many pages you want to get: '))
    pool = redis.ConnectionPool(host='127.0.0.1',port=6379,decode_responses=True)
    #创建链接对象
    redis_r=redis.Redis(connection_pool=pool)
    getXCProxyIp(page)
