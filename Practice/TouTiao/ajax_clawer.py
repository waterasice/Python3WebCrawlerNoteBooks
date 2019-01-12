import requests
from urllib.parse import urlencode
import json
from hashlib import md5
from bs4 import BeautifulSoup
import re
import os
from requests.exceptions import RequestException
import pymongo
from config import *
from multiprocessing import Pool
client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
def get_page_first(offest,keyword):#抓取首页
    data={
        'offset':offest,  #offest可变
        'format':'json',
        'keyword':keyword,#keyword是可以从config,py文件中定义
        'autoload':'true',
        'count':'20',
        'cur_tab':3
    }
    url='http://www.toutiao.com/search_content/?'+urlencode(data)
    try:
        response=requests.get(url) #请求url
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求异常')
        return None
def parse_page_first(html):
    data=json.loads(html)#转换成json对象
    if data and 'data' in data.keys():
        for item in data.get('data'):#data这个对象非空 并且 这个对象里有叫'data'的key
            yield item.get('article_url')
def get_page_detai(url):
    try:
        response=requests.get(url) #请求url
        if response.status_code==200:
            return response.text
        return None
    except RequestException:
        print('请求异常')
        return None
def parse_page_chirld(htmlchirld,url):
    soup=BeautifulSoup(htmlchirld,'lxml')
    title=soup.select('title')[0].get_text()
    print(title)
    print(htmlchirld)
    images_pattern=re.compile('gallery: (.*?),\n',re.S)
    result = re.search(images_pattern, htmlchirld)
    print(result)
    if result:#判断是否成功
        result = result.group(1)
        result = result[12:]
        result = result[:-2]
        result = re.sub(r'\\','',result)
#        print(result)
        data = json.loads(result)  # 对字符串进行解析，把字符串转化成json对象
 #       print(data)
        if data and 'sub_images' in data.keys():  # 判断里面是否含有我们想要的数据
            sub_images = data.get('sub_images')
            images_url=[item.get('url') for item in sub_images]
            for image in images_url: 
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images_url': images_url
            }
def download_image(url):
    print('正在下载',url)
    try:
        response=requests.get(url)
        if response.status_code==200:
            #return response.text
            save_image(response.content)#content二进制
        return None
    except RequestException:
        print('请求图片出错',url)
        return None

def save_to_mongo(result):
    if db[MONGO_TABLE].insert(result):
        print('储存mongodb成功',result)
        return True
    return False
def save_image(content):
    file_path='{0}/{1}.{2}'.format('./',md5(content).hexdigest(),'jpg')
    if not os.path.exists(file_path):
        with open(file_path,'wb') as f:
            f.write(content)
            f.close()
def main(offset):
    html=get_page_first(offset,KEYWORD)
    print(html)
    for url in parse_page_first(html):
        htmlchirld=get_page_detai(url)
        if htmlchirld:
            result=parse_page_chirld(htmlchirld,url)
            if result:
                save_to_mongo(result)

if __name__=='__main__':
#    for x in range(GROUP_START,GROUP_END+1):
#        main(x*20)
    p = Pool()
    offsets = [offset for offset in range(0,100,20)]
    p.map_async(main,offsets)
    p.close()
    p.join()
