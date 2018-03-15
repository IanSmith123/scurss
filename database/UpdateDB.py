"""
通过比对刚刚爬取到的内容和数据库取出来的内容
来检查数据库的每条记录是否有更新
"""
import hashlib

import arrow


class UpdateDB(object):
    """
    更新数据库信息
    """

    def __init__(self, table, info, conn):
        self.info = info
        self.update = []
        self.new = []
        self.table = table
        self.conn = conn

    def check_update(self):
        """

        :return: json list 包含所有的有更新的网站的原始内容

        不提供网站修改的前后的变化
        """
        cur = self.conn.cursor()

        # 获取所有新闻的id
        sql = """
          select newsid from {}""".format(self.table)
        cur.execute(sql)

        all_newsid = [item[0] for item in cur.fetchall()]

        # 做set的交操作，获取所有存在的新闻的id
        exist_id = set(all_newsid) & set([news['id'] for news in self.info])

        # 提取出新出来的新闻的列表
        for news in self.info:
            # 不存在set里面说明是新公布的
            if news['id'] not in exist_id:
                self.new.append(news)
                print("新公布的新闻id ", news['id'])
            else:
                # 存在更新内容的
                sql = """
                  select newscontent from {} where newsid='{}'""".format(self.table, news['id'])
                cur.execute(sql)
                content = cur.fetchall()[0][0]

                if hashlib.md5(content.encode('utf-8')).hexdigest() != hashlib.md5(news['content'].encode('utf-8')).hexdigest():
                    self.update.append(news)
                    print('更新了以前的新闻的内容的id ', news['id'])
        # 插入数据库的时候需要注意，最后更新全部消息的爬虫更新时间

        return self.new, self.update

    # 测试完成
    def update_db_last_check_time(self, conn, *table):
        """
        更新新闻表的last_check_time字段
        :param conn: 传入一个psycopg2的连接对象
        :param table: 需要更新的表名字
        :return:
        """
        cur = conn.cursor()

        now = arrow.now().timestamp
        for tb in table:
            sql = """
            update {} set lastchecktime={} """.format(tb, now)
            cur.execute(sql)

        conn.commit()

    def insert_update_news(self, conn, table, info):
        """
        修改发生了更新的消息
        :param conn: 传入一个数据库连接对象
        :param table: 要更新的表名
        :param info: 表的对象
        :return:
        """
        cur = conn.cursor()

        # 查一下更新的语法2333
        for news in info:
            # print(news)
            sql = """
            update {} set newstitle = '{}',newscontent='{}',lastupdatetime='{}' where newsid='{}'""".format \
                (table, news['title'], news['content'], repr(arrow.get().timestamp), news['id'])
            cur.execute(sql)

        conn.commit()

    def insert_new_news(self, conn, table, info):
        """
        插入新的公布的消息
        :param conn: 数据库连接对象
        :param table: 待更新的表名
        :param info: json对象，包含所有要更新的条目
        :return:
        """

        cur = conn.cursor()
        for news in info:
            sql = """
                INSERT INTO {} 
        (newsid, newstitle, newscontent, newsurl, lastupdatetime, publishtime)  
            VALUES ('{}', '{}', '{}', '{}', '{}', '{}')""". \
                format(table, news['id'], news['title'], news['content'], news['url'], news['date'], news['date'])

            cur.execute(sql)
        print("--" * 20)

        conn.commit()

