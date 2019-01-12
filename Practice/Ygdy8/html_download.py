import urllib.request
class HtmlDownloader(object):
    def download(self, url):
        if url is None:                                         #合理性判断
            return None
        response = urllib.request.urlopen(url)                  #最简单的下载方式下载网页
        if response .getcode()!=200:
            return None
        return response.read()                                  #返回网页内容
