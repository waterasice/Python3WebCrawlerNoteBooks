import re                                                               #导入正则
from urllib.parse import urljoin                                        #导入parse的urljoin
from bs4 import BeautifulSoup                                           #导入beautifulsoup

class HtmlParser(object):
    def _get_new_urls(self, page_url, soup):                            #得到新的待处理url
        new_urls = set()                                                #定义空set
        # <a href="/html/gndy/jddy/20161007/52168.html" class="ulink">
        links = soup.find_all('a',href=re.compile(r"/html/gndy/jddy/2016\d{4}/\d{4,6}.html"))#正则匹配
        for link in links :                                             #链接匹配的话
            new_url = link['href']
            new_full_url = urljoin(page_url,new_url)                    #new_url已page_urrl的形式拼成新链接
            # print(new_full_url)                                       #调试用
            new_urls.add(new_full_url)                                  #拼成的新链接添加进new_urls
        return new_urls

    def _get_new_data(self, page_url, soup):
        res_data = {}                                                   #保留的数据
        temp_data =[]                                                   #临时存放
        #url
        res_data['url']=page_url                                        #爬到的网址
        res_data['title'] = soup.title                                  #网址title
        temp_data=[x for x in res_data['title']]                        #转换成list
        res_data['title']= temp_data                                    #为了能够输出html再转回字典
        return  res_data


    def parse(self, page_url, html_cont):
       if page_url is None or html_cont is None:                        #合理性判断
           return
       soup = BeautifulSoup(html_cont,'html.parser',from_encoding='gbk')#解码方式，电影天堂是gbk
       new_urls = self._get_new_urls(page_url,soup)                     #调用上面的方法
       new_data = self._get_new_data(page_url,soup)

       return new_urls,new_data                                         #解析完成返回数据
