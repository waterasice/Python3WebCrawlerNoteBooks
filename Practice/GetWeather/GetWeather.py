# coding = utf8
import requests
from requests.exceptions import RequestException
from lxml import html
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from datetime import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig(level=logging.DEBUG)
 
my_sender='penggang@csg.com.cn'    
my_pass = '********'              
my_user='823301766@qq.com'      
NanJiWEATHER_URL = "http://www.weather.com.cn/weather/101190101.shtml"

def create_db_table():        
    db = pymysql.connect("localhost","root","12345","TESTDB")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS NANJING_WEATHER")
    sql = """CREATE TABLE NANJING_WEATHER(\
            TIME VARCHAR(30),
           WEATHER VARCHAR(30)
            ) """
    cursor.execute(sql)
    logging.debug(datetime.now().strftime("%y-%m-%d %H:%M:%S"))
    db.close()

def insert_db_table(data):
    now = datetime.now().strftime("%y-%m-%d %H:%M:%S")
    data = data
    logging.debug(data)
    db = pymysql.connect("localhost","root","12345","TESTDB")  
    cursor = db.cursor()
    sql = "INSERT INTO NANJING_WEATHER(TIME,\
          WEATHER) \
         VALUES ('%s','%s') " % (now,data)
    try:
        cursor.execute(sql)
        db.commit()
        logging.debug("insert successed")
    except :
        db.rollback()
        logging.debug ('insert failed')
    db.close()
def select_db_table():
    db = pymysql.connect("localhost","root","12345","TESTDB")  
    cursor = db.cursor()
    sql = "SELECT * from NANJING_WEATHER"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        logging.debug(result)
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
            logging.debug(response.encoding)
            logging.debug(response.apparent_encoding)
            r = response.text
            rr = r.encode('ISO-8859-1').decode(response.apparent_encoding)
            tree = html.fromstring(rr)
            el=tree.xpath('//div[@id="7d"]//input[@type="hidden"]')
            logging.debug(el[0].value)
            logging.debug(len(el[0].value))
            return el[0].value
        return None
    except RequestException:
        logging.debug('load weather failed')
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
def main():
    weather =  get_weather(NanJiWEATHER_URL)
    insert_db_table(weather)
    mail(weather)

if __name__ == '__main__':
    create_db_table()
    scheduler = BlockingScheduler()
    scheduler.add_job(main,'cron',day_of_week='1-7',hour=7,minute=30)
    scheduler.start()
    
		
