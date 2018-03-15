# coding:utf-8
import os
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import re

import arrow

class SendEmail(object):
    def __init__(self):

        self.email_user = os.environ["EMAIL_USER"]
        self.email_passwd = os.environ["EMAIL_PASSWD"]
        self.mail_server = os.environ["MAIL_SERVER"]
        self.sender_name = os.environ["SENDER_NAME"]


    def send_mail(self, mail_recv, mail_content):
        """

        :param mail_recv: str, 单个用户的邮箱地址
        :param mail_content: str, 发送的邮件的完整内容
        :return:
        """
        message = MIMEText(mail_content, 'plain', 'utf-8')
        message['From'] = Header("{}".format(self.email_user))
        
        message['To'] = Header("{}".format(mail_recv))

        subject = "在 {} 学校网站更新啦~(￣▽￣)~*".format(arrow.now('Asia/Shanghai').format('YYYY-MM-DD HH:mm:ss'))
        message['Subject'] = Header(subject)

        # print(message)
        # send
        sender = smtplib.SMTP(self.mail_server, 25)
        sender.login(self.email_user, self.email_passwd)
        sender.sendmail(self.sender_name, [mail_recv], message.as_string())

    def get_user_info(self, conn):
        cur = conn.cursor()
        sql = """
        select usermail, regtime, subscribelist from userlist order by regtime desc"""
        cur.execute(sql)
        userinfo = cur.fetchall()
        # print(userinfo)
        # userlist = [{"mail": item('usermail'),"subscribelist":item["subscribelist"]} for item in userinfo]

        # 邮箱去重
        mail_pool = {item[0] for item in userinfo}
        vilid_mail = []
        for mail in userinfo:
            if mail[0] in mail_pool:
                vilid_mail.append(mail)
                mail_pool.remove(mail[0])
            else:
                continue
        # 验证邮箱有效性, 格式化数据
        print('mail_all', userinfo)
        print('vilid_mail', vilid_mail)

        reg = r'[^@]+@[^@]+\.[^@]+'
        userlist = [{"mail": item[0], "subscribelist": item[-1].split(',')} for item in vilid_mail if re.findall(reg, item[0])]


        print("数据库中存在记录的用户的信息邮箱和订阅的主题", userlist)
        return userlist




