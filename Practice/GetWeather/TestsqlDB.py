#!/bin/python3
# coding = 'utf-8'

import pymysql
def create_db_table():         #创建数据库 表格，TESTDB需要提前创建
    db = pymysql.connect("localhost","root","12345","TESTDB")
    cursor = db.cursor()
    cursor.execute("DROP TABLE IF EXISTS NANJING_WEATHER")
    sql = """CREATE TABLE NANJING_WEATHER(\
            TIME CHAR(30),
           WEATHER CHAR(30)
            ) """
    cursor.execute(sql)
    db.close()

if __name__ =='__main__':
    create_db_table()
    db = pymysql.connect("localhost","root","12345","TESTDB")  
    cursor = db.cursor()
    sql = "INSERT INTO NANJING_WEATHER(TIME,\
          WEATHER) \
         VALUES ('%s','%s') " % ('2017-12-08','晴朗')
    try:
        cursor.execute(sql)
        db.commit()
        print("info")
    except :
        db.rollback()
    sql = "SELECT * from NANJING_WEATHER"
    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        db.commit()
        print(result)
    except :
        db.rollback()
    db.close()
