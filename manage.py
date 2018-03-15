import json
import uuid
import traceback
import re
import time

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import arrow
import redis

from spider.jwc import JwcSpider
from spider.cs import CsSpider
from spider.xsc import XscSpider

from database.UpdateDB import UpdateDB
from database.CreateDB import CreateDB
from send_mail.send_mail import SendEmail

from feed_gen.GenRss import GenRss


class Manage(object):
    """
    管理整个爬虫，包括信息采集，数据库插入
    最后需要检测是否需要推送消息到客户并且完成邮件推送
    """

    def __init__(self):
        self.jwc_info = ''
        self.xsc_info = ''
        self.cs_info = ''

        self.jwc_update = ''
        self.xsc_update = ''
        self.cs_update = ''

        self.jwc_new = ''
        self.xsc_new = ''
        self.cs_new = ''

        self.user_list = []
        # 每次一新建需要数据库操作的对象的时候需要将conn对象传入
        # self.conn = psycopg2.connect(database='scurss', user='postgres', password='ms17010', host='b.17010.tk',
        #                             port='5432')

        # self.create_db = psycopg2.connect(user='postgres', password='ms17010', host='108ed.les1ie.com', port='5432')
        self.create_db = psycopg2.connect(user='postgres', password='ms17010', host='pgsqldb', port='5432')
        self.create_db.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        CreateDB.create_db(self.create_db)


        self.conn = psycopg2.connect(database='scurss', user='postgres', password='ms17010', host='pgsqldb',
                                     port='5432')

        # self.conn = psycopg2.connect(database='scurss', user='postgres', password='ms17010', host='108ed.les1ie.com',
         #                             port='5432')

        self.init_db = CreateDB.create_table(self.conn)

        self.update_db = UpdateDB('jwc', self.jwc_info, self.conn)

    def close_db(self):
        self.conn.close()

    def crawl_all(self):
        """
        爬取所有的网站
        :return
        """
        jwc = JwcSpider()
        self.jwc_info = jwc.crawl()

        cs = CsSpider()
        self.cs_info = cs.crawl()

        xsc = XscSpider()
        self.xsc_info = xsc.crawl()

    def fake_crawl_all(self):
        """
        网速太慢了，使用本机缓存的jwc信息吧，每次存数据库测试都本机解析，不用去爬教务处
        :return:
        """
        with open('database/jwc.json', 'r') as f:
            j = f.read()
            self.jwc_info = json.loads(j)
            # self.jwc_new = self.jwc_info
            print("载入缓存jwc_info完成")

    def fake_update(self):
        with open('database/update.json', 'r') as f:
            self.jwc_update = json.loads(f.read())

        old_id = []
        for i in self.jwc_info:
            old_id.append(i['id'])
        new_id = []
        for j in self.jwc_update:
            new_id = j['id']
        diff = set(old_id) & set(new_id)
        renew = []
        for new in self.jwc_update:
            if new['id'] not in diff:
                renew.append(new)

        self.jwc_update = renew

    def check_update(self):
        # 检查教务处新公布的新闻和更新了内容的新闻
        # jwc_check = UpdateDB("jwc", self.info, self.conn)
        check_jwc = UpdateDB("jwcnews", self.jwc_info, self.conn)
        self.jwc_new, self.jwc_update = check_jwc.check_update()

        check_cs = UpdateDB("csnews", self.cs_info, self.conn)
        self.cs_new, self.cs_update = check_cs.check_update()

        check_xsc = UpdateDB("xscnews", self.xsc_info, self.conn)
        self.xsc_new, self.xsc_update = check_xsc.check_update()


    # todo: 测试
    def update_db_checktime(self):
        """
        升级所有表的最后检查更新时间， last_check_time字段
        :return:
        """
        # 传入一个kwargs
        self.update_db.update_db_last_check_time(self.conn, "jwcnews", "xscnews", "csnews")
        # self.update_db.update_db_last_check_time(self.conn, "jwcnews")


    def insert_update_news_info(self):
        """
        升级刚刚检测到更新了的新闻
        :return:
        """
        self.update_db.insert_update_news(self.conn, "jwcnews", self.jwc_update)
        print("插入教务处更新的新闻完成")
        self.update_db.insert_update_news(self.conn, "csnews", self.cs_update)
        print("插入计算机学院更新的新闻完成")
        self.update_db.insert_update_news(self.conn, "xscnews", self.xsc_update)
        print("插入学工部更新的新闻完成")


    def insert_new_news_info(self):
        """
        插入新公布的新闻
        :return:
        """
        #        self.update_db.insert_new_news(self.conn, "jwcnews", self.jwc_new)
        self.update_db.insert_new_news(self.conn, "jwcnews", self.jwc_new)
        print("插入教务处新公布的新闻完成")

        self.update_db.insert_new_news(self.conn, "csnews", self.cs_new)
        print("插入计算机学院官网新公布的新闻完成")
        self.update_db.insert_new_news(self.conn, "xscnews", self.xsc_new)
        print("插入学工部新公布的新闻完成")

    def get_user_info(self):
        """
        获取订阅了的用户列表
        :return:
        """
        getter = SendEmail()
        self.user_list = getter.get_user_info(self.conn)

    def send_mail(self):
        sender = SendEmail()

        # 发送邮件的格式： 用户的邮箱地址列表， 用户需要的信息
        # sender.send_mail(self.jwc_user, self.jwc_to_send)
        mail_queue = []
        for user in self.user_list:
            tmp_queue = []

            tmp_update = []
            tmp_new = []
            for scribe in user['subscribelist']:
                # print(self.jwc_update)
                if scribe == 'jwcnews':
                    tmp_update.append([item['title']+' '+item['url'] + ' \n' for item in self.jwc_update])
                    tmp_new.append([item['title']+' '+item['url'] + ' \n' for item in self.jwc_new])

                if scribe == 'xgbnews':
                    tmp_update.append([item['title']+' '+item['url'] + ' \n' for item in self.xsc_update])
                    tmp_new.append([item['title']+' '+item['url'] + ' \n' for item in self.xsc_new])

                if scribe == 'csnews':
                    tmp_update.append([item['title']+' '+item['url'] + ' \n' for item in self.cs_update])
                    tmp_new.append([item['title']+' '+item['url'] + ' \n' for item in self.cs_new])

            # 需要发送的消息包括更新的新闻的标题和新闻的链接地址
            # 为了消除空的列表 [[],[],[]]这种的影响，强行判断一下
            if len(repr(tmp_update)) > 30:
                renew = '发生了更新的新闻: \n'
                for news in tmp_update:
                    if news:
                        print(news)
                        for _ in news:
                            renew = renew + _
                    else:
                        print("这是一个长度为0的news")
                        continue
            else:
                renew = ''

            if len(repr(tmp_new))>30:
                new = "新公布的新闻: \n"
                for news in tmp_new:
                    if news:
                        for _ in news:
                            new = new + _
                    else:
                        print("长度为0的新公布的新闻")
                        continue

            else:
                new = ''
            if renew or new:
                tmp_queue.append(
                    {
                        'mail': user['mail'],
                        'info':  renew + '\n' + new + "\n 退订请手动发送邮件到 iansmith@qq.com"
                    }
                )
            else:
                tmp_queue = []

            for _ in tmp_queue:
                mail_queue.append(_)
        print("mail queue ", mail_queue)

        if mail_queue:
            for user in mail_queue:
                try:
                    sender.send_mail(user['mail'], user['info'])
                    print('send to ', user['mail'])

                except:
                    traceback.print_exc()
                    print("send fail")
        else:
            print("没有新闻更新，无需推送邮件")


    def create_sample_reg_user(self):
        cur = self.conn.cursor()
        sql = """
        insert into userlist \
        (uuid, username, regtime, usermail, subscribelist) \
        values ('{}', '{}', '{}', '{}', '{}')""".format(
            uuid.uuid4().hex, 'Les1ie', repr(arrow.get().timestamp), 'iansmith@qq.com', 'xgbnews,jwcnews,csnews'
        )
        cur.execute(sql)

        sql = """
        insert into userlist \
        (uuid, username, regtime, usermail, subscribelist) \
        values ('{}', '{}', '{}', '{}', '{}')""".format(
            uuid.uuid4().hex, 'Les1ie', repr(arrow.get().timestamp), 'tdxceg08521@chacuo.net', 'jwcnews,csnews'
        )
        # cur.execute(sql)
        self.conn.commit()

    def generate_feed_xml(self):
        feed = GenRss()
        feed.get_news_list()
        feed.gen_rss()
        feed.close_db()


def main():
    manage = Manage()
    # 开始爬行
    # manage.fake_crawl_all()
    # manage.fake_update()
    try:
        print("SCURSS爬虫开始工作啦")
        manage.crawl_all()

    #     print(manage.jwc_new)
    #     print(manage.jwc_update)
    #    manage.insert_new_news_info()
        # 对比数据库检测更新
        manage.check_update()
        # 插入更新了的新闻
        manage.insert_update_news_info()
        # 插入新出现的新闻
        manage.insert_new_news_info()
        # 更新数据库中全局的检查时间
        manage.update_db_checktime()

        # 获取订阅的用户信息
        manage.create_sample_reg_user()
        manage.get_user_info()
        print("生成feed文件")
        manage.generate_feed_xml()
        # 发送邮件
        manage.send_mail()
        print("操作完成")

    finally:
        manage.close_db()
        print("> 关闭数据库连接完成...")

if __name__ == '__main__':
    main()
    print("一次工作完成", arrow.now('Asia/Shanghai').format("YYYY-MM-DD HH:mm:ss"))
    time.sleep(60*60*2)
