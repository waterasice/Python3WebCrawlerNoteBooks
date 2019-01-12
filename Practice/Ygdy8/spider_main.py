from spider_dianying import url_manager,html_downloader, html_parser, html_outputer

class  SpiderMain():
    def __init__(self):                                         #初始化
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self,root_url):                                    #爬取函数，参数root_url为爬取的起始网址
        count = 1                                               #爬取数量
        self.urls.add_new_url(root_url)                         #添加待爬取的url
        while self.urls.has_new_url():                          #判断存在未爬取的url就进行数据采集和新url采集
            try:                                                #像404等异常可能发生
                new_url= self.urls.get_new_url()                #得到新url
                print("craw %d : %s" % (count, new_url))        #控制台打印输出
                html_cont = self.downloader.download(new_url)   #下载新url内容
                new_urls,new_data = self.parser.parse(new_url,html_cont)#解析新内容
                self.urls.add_new_urls(new_urls)                #解析得到的再加入新的urls列表中
                self.outputer.collect_data(new_data)            #收集数据
                if count==100:                                  #100个则退出
                    break
                count=count+1
            except :
                print("craw failed")                            #异常打印爬取失败
        self.outputer.output_html()                             #收集到的数据输出成html格式


if __name__=="__main__":
    root_url="http://www.ygdy8.net/html/gndy/china/index.html"  #爬取入口
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)                                   #开始爬取
