class UrlManager(object):

    def __init__(self):
        self.new_urls=set()                                         #初始为空的set
        self.old_urls=set()

    def add_new_url(self, url):                                     #添加新的url
        if url is None :
            return
        if url not in self.new_urls and url not in self.old_urls:   #并未爬取过的url才添加
            self.new_urls.add(url)                                  #set的添加方法


    def add_new_urls(self, urls):                                   #爬取不为空批量添加
        if urls is None or len(urls) ==0:
            return
        for url in urls:
            self.add_new_url(url)                                   #调用单个添加方法


    def has_new_url(self):
       return  len(self.new_urls)!=0                                #判断是否有url

    def get_new_url(self):                                          #得到url
        new_url = self.new_urls.pop()                               #刚刚下载的pop出
        self.old_urls.add(new_url)                                  #同时放入old_url，代表已经处理过
        return new_url                                              #返回

