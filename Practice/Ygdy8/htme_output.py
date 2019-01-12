#coding=utf8
class HtmlOutputer(object):
    def __init__(self):
        self.datas = []                                              #定义空数据list

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)                                      #合理就添加

    def output_html(self):
       fout = open('output.html','w' ,encoding='utf8')              #编码方式utf-8
       fout.write('<html>')
       fout.write("<head><meta http-equiv=\"content-type\" content=\"text/html;charset=utf-8\"></head>")
       fout.write('<body>')                                         #上面这句在Python3中必须要有，否则网页输出byte码
       fout.write('<table>')                                        #而不是汉字

       for data in self.datas:
           fout.write('<tr>')
           fout.write('<td>%s</td>' % data['url'])                  #网址
           fout.write('<td>%s</td>' % data['title'])                #title
           fout.write('</tr>')
       fout.write('</table>')
       fout.write('</body>')
       fout.write('</html>')

       fout.close()                                                 #关闭
