import os
import re
import json

import smtplib
from email.mime.text import MIMEText
from email.header import Header

import arrow
import redis
import psycopg2
from flask import Flask

app = Flask(__name__)

class Sync_pg_redis(object):
    """
    主类,管理数据库连接
    """

    def __init__(self):

        self.email_user = 'm15528690575@163.com'
        self.email_passwd = 'test123'
        self.mail_server = 'smtp.163.com'
        self.sender_name = "m15528690575@163.com"

        self.email_user = os.environ["EMAIL_USER"]
        self.email_passwd = os.environ["EMAIL_PASSWD"]
        self.mail_server = os.environ["MAIL_SERVER"]
        self.sender_name = os.environ["SENDER_NAME"]


        try:
            self.r = redis.StrictRedis(host="mail_redis", port=6379, db=1)
            print("connect success redis")

        except:
            self.r = redis.StrictRedis(host="108ed.les1ie.com", port=6378, db=1)
            print("connect success redis, 108ed")

        self.pg = psycopg2.connect(host="pgsqldb", port=5432, database='scurss', user='postgres', password='ms17010')
#        self.pg = psycopg2.connect(host="108ed.les1ie.com", port='5432', database='scurss', user='postgres', password='ms17010')
        print("con to pg success")


    def get_new_user_list(self):
        log = ''
        cur = self.pg.cursor()

        sql = """
                select usermail, regtime, subscribelist from userlist order by regtime desc"""
        cur.execute(sql)
        print("get all user info")

        userinfo = cur.fetchall()

        mail_pool = {item[0] for item in userinfo}
        vilid_mail = []
        for mail in userinfo:
            if mail[0] in mail_pool:
                vilid_mail.append(mail)
                mail_pool.remove(mail[0])
            else:
                continue

        reg = r'[^@]+@[^@]+\.[^@]+'
        userlist = [{"mail": item[0], "subscribelist": item[-1].split(',')} for item in vilid_mail if
                    re.findall(reg, item[0])]

        # 获取redis中缓存的信息
        redis_mail_info = self.r.get("userlist")
        if redis_mail_info:
            log += 'redis的mail_info不为空'
            redis_mail_info = eval(self.r.get("userlist"))
        else:
            redis_mail_info = ''

        # 如何验证同一个用户的邮箱未改变但是订阅内容改变了，检测用户增加
        if redis_mail_info:
            new_user = [item for item in userlist if item not in redis_mail_info]
        else:
            new_user = userlist

        # redis缓存的数据中用户数比postgres中的少


        # 更新redis中缓存的用户列表信息

        self.r.set("userlist", json.dumps(userlist))
        print(userlist)

        return new_user


    def get_news_list(self):
        """
        三个新闻表中每个表中最新的十条新闻
        :return:
        """
        cur = self.pg.cursor()
        all_news = []
        for table in ['jwcnews', 'csnews', 'xscnews']:
            sql = """
            SELECT newstitle, newsurl, publishtime from {} ORDER BY publishtime desc LIMIT 10;
        """.format(table)
            cur.execute(sql)
            for news in cur.fetchall():
                all_news.append({'title': news[0], 'url': news[1]})
        # print(all_news)
        # 组装成为文本
        web_content = '欢迎关注SCURSS, 这是目前教务处，学工部，计算机学院官网的最新新闻 \n '

        for item in all_news:
            web_content = web_content + item['title'] + item['url'] + ' \n '
        return web_content

    def send_init_mail(self, mail_recv, mail_content):
        """
        :param mail_recv: str, 单个用户的邮箱地址
        :param mail_content: str, 发送的邮件的完整内容
        :return:
        """
        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['From'] = Header("{}".format(self.email_user))
        # message['To'] = Header("SCURSS-user")
        message['To'] = Header("{}".format(mail_recv))

        subject = "在 {} 学校网站又又又又更新了".format(arrow.now('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss'))
        message['Subject'] = Header(subject)

        # print(message)
        # send
        sender = smtplib.SMTP(self.mail_server, 25)
        sender.login(self.email_user, self.email_passwd)
        sender.sendmail(self.sender_name, [mail_recv], message.as_string())

    def close_db(self):
        self.pg.close()


@app.route('/reg', methods=['GET', 'POST'])
def new_reg():
    s = Sync_pg_redis()

    new_user = s.get_new_user_list()
    news_content = s.get_news_list()
    if new_user:
        for user in new_user:
            s.send_init_mail(user['mail'], news_content)

#    return "新注册的用户" + repr(new_user)
    return "一切搞定~ 首先给你一份包含了所有网站的邮件看看~ "

@app.route('/test', methods=['GET', 'POST'])
def test():
    s = Sync_pg_redis()
    s.get_news_list()

    return repr(s.get_news_list())

@app.route('/', methods=['GET'])
def hhh():
    return "It works!"

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=80, debug=True)


