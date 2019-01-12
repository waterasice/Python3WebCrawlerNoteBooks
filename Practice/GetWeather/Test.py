# coding = utf-8
import requests
from lxml import html
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
 
my_sender='xxx@163.com'    
my_pass = 'xxxxxx'              
my_user='xxx@qq.com'      
NanJiWEATHER_URL = "http://www.weather.com.cn/weather/101190101.shtml"

def create_db_table():        
    db = pymysql.connect("localhost","root","12345","TESTDB")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS NANJING_WEATHER")
    sql = """CREATE TABLE NANJING_WEATHER(\
            TIME CHAR(50),
           WEATHER CHAR(50)
            ) """
    cursor.execute(sql)
    print(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
    db.close()

def insert_db_table(data):
    now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    db = pymysql.connect("localhost","root","12345","TESTDB")  
    cursor = db.cursor()
    sql = "INSERT INTO NANJING_WEATHER(TIME,\
          WEATHER) \
         VALUES ('%s','%s') " % (now,data)
    try:
        cursor.execute(sql)
        db.commit()
        print("info")
    except :
        db.rollback()
        print('insert failed')
    db.close()
def select_db_table():
    db = pymysql.connect("localhost","root","12345","TESTDB")  
    cursor = db.cursor()
    sql = "SELECT * from NANJING_WEATHER"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        print(result)
        return result
    except :
        db.rollback()
        return None
    db.close()
def get_weather(url):
	headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }
	try:
	    response=requests.get(NanJiWEATHER_URL,headers=headers) 
	    if response.status_code == 200:
                print(response.encoding)
                print(response.apparent_encoding)
                r = response.text
                rr = r.encode('ISO-8859-1').decode(response.apparent_encoding)
                tree = html.fromstring(rr)
                el=tree.xpath('//div[@id="7d"]//input[@type="hidden"]')
           # return el[0].value.encode('utf-8')
                return el[0].value
           # return None
        except RequestException:
		print('failed')
		return None
def mail(maintext):
    ret=True
    try:
        msg=MIMEText(maintext,'plain','utf-8')
        msg['From']=formataddr(["FromPG's script",my_sender]) 
        msg['To']=formataddr(["FK",my_user])             
        msg['Subject']="Script send email"               
 
        server=smtplib.SMTP_SSL("smtp.exmail.qq.com", 465) 
        server.login(my_sender, my_pass) 
        server.sendmail(my_sender,[my_user,],msg.as_string())  
        server.quit()  
    except Exception:  
        ret=False
    return ret
 

if __name__ == '__main__':
    create_db_table()
    weather =  get_weather(NanJiWEATHER_URL)
    insert_db_table(weather)
   
		
