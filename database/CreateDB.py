import psycopg2
import json


class CreateDB(object):
    def __init__(self):
        # self.conn = psycopg2.connect(database='scurss', user='postgres', password='ms17010', host='172.17.0.3', port='5432')

        # docker 环境
        # self.conn = psycopg2.connect(database='scurss', user='postgres', password='ms17010', host='108ed.les1ie.com', port='5432')

        pass

    def create_table(conn):
        """
        用于初始化数据库
        :return:
        """

        cur = conn.cursor()

        # 创建表 jwc
        cur.execute('''
        create TABLE IF NOT EXISTS jwcNews (
  newsId TEXT NOT NULL PRIMARY KEY,
  newsTitle text NOT NULL,
  newsContent text NOT NULL,
  newsUrl text NOT NULL,
  lastCheckTime TEXT,
  lastUpdateTime TEXT,
  publishTime TEXT NOT NULL
)
        ''')
        # 创建表 csnews
        cur.execute('''
        create TABLE IF NOT EXISTS csnews (
  newsId TEXT NOT NULL PRIMARY KEY,
  newsTitle text NOT NULL,
  newsContent text NOT NULL,
  newsUrl text NOT NULL,
  lastCheckTime TEXT,
  lastUpdateTime TEXT,
  publishTime TEXT NOT NULL
)
        ''')
        # 创建表 xscnews

        cur.execute('''
        create TABLE IF NOT EXISTS xscnews (
  newsId TEXT NOT NULL PRIMARY KEY,
  newsTitle text NOT NULL,
  newsContent text NOT NULL,
  newsUrl text NOT NULL,
  lastCheckTime TEXT,
  lastUpdateTime TEXT,
  publishTime TEXT NOT NULL
)
        ''')

        # 创建表 userlist
        cur.execute('''
        CREATE table IF NOT EXISTS UserList (
  uuid text not NULL PRIMARY KEY ,
  userName text NOT NULL ,
  regTime text not null,
  usermail text not null,
  subscribelist text not null
)
        ''')
        # 创建建议网站 tocrawl
        cur.execute('''
        CREATE TABLE IF NOT EXISTS tocrawl (
  uuid TEXT not null PRIMARY KEY ,
  username TEXT not null,
  commiturl TEXT not NULL
)
      ''')

        conn.commit()
        print("create table finish")

    def create_db(conn):
        sql = """
              select datname from pg_catalog.pg_database where datname='scurss'"""
        cur = conn.cursor()
        cur.execute(sql)
        if cur.fetchall():
            print("数据库存在，无需新建")
        else:
            cur.execute("create database scurss")
            print("新建数据库完成")
        conn.commit()
        conn.close()
    def insert_userlist(self):
        """
        插入订阅的用户信息
        :return:
        """
        pass
