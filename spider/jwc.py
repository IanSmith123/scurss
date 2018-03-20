import re
import json
from time import time, sleep
import arrow
from lxml import etree

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions


class JwcSpider:
    def __init__(self):
        self.url = "http://ip.cn"
        self.url = "https://httpbin.org/headers"
        self.url = "http://jwc.scu.edu.cn/jwc/frontPage.action"
        # self.driver = self.init_phantom_driver()
        # self.driver = self.init_chrome_driver()
        self.driver = self.init_firefox_driver()

    def init_chrome_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--windows-size=1920*1080")
        options.add_argument("User-Agent= https://scurss.17010.tk Les1ie just wanna do something for we students. :)")
        driver = webdriver.Chrome(chrome_options=options)
        return driver

    def init_phantom_driver(self):
        return webdriver.PhantomJS()
        headers = {
            "User-Agent":  "Mozilla/5.0 https://scurss.17010.tk Les1ie just wanna do something for we students :)"
        }
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = headers["User-Agent"]
        driver = webdriver.PhantomJS()
        driver.set_window_size(1920, 1080)
        return driver

    def init_firefox_driver(self):
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.add_argument("--windows-size=1920*1080")
        options.add_argument("User-Agent= https://scurss.17010.tk Les1ie just wanna do something for we students. :)")
        driver = webdriver.Firefox(firefox_options=options)

        return driver

    def get_page_src(self, url):
        self.driver.get(url)
        # print(self.driver.page_source)
        # return self.driver.page_source
        try:
            WebDriverWait(self.driver, 10).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, "STYLE3"))
            )
        except:
            print(self.driver.page_source)
            print("time out error")
        return self.driver.page_source

    def crawl(self):
        """
        用到时间的地方一律采用时间戳的方式存储

        :return [{"news_title":"xxxx", "news_date":int timestamp, "news_url":"url"}, ]
        """
        start_time = time()
        r = self.get_page_src(self.url)
        tree = etree.HTML(r)
        # sleep(100)

        self.news_title = tree.xpath("//tr/td/span[@class='STYLE4']/a/span[position()=1]/text()")
        self.news_url = tree.xpath("//tr/td/span[@class='STYLE4']/a/@href")
        self.news_date = tree.xpath("//tr/td[@class='STYLE4']/font/text()")

        web_content = []
        reg = r'id=(\d+)$'
        #        reg = r'([0-9]*)$'
        for i in range(len(self.news_title)):
            # 从news.id中提取id编号作为主码
            news_id = re.findall(reg, self.news_url[i])[0]

            # 将时间转换为时间戳
            date = repr(arrow.get(self.news_date[i]).timestamp)

            # 拼凑url 为完整的url
            n_url = "http://jwc.scu.edu.cn/jwc/" + self.news_url[i]

            dic = {"id": news_id, "title": self.news_title[i], "url": n_url, "date": date, "content": ''}
            web_content.append(dic)

        # print(web_content)
        print("成功获取到jwc首页内容, 长度为" + repr(len(web_content)) + "用时 " + repr(time() - start_time) + ' s')

        # 获取每一条新闻的内容信息
        for i in range(len(web_content)):
            news_url = "http://jwc.scu.edu.cn/jwc/" + web_content[i]["url"]

            # r = requests.get(news_url, timeout=5)
            r = self.get_page_src(news_url)
            tree = etree.HTML(r)

            con = tree.xpath("//input[@name='news.content']/@value")

            web_content[i]['content'] = con[0]
            print(web_content)

        print("完成获取jwc每条新闻的具体内容, 用时 " + repr(time() - start_time) + ' s')

        # with open("update.json", 'w') as f:
         #    f.write(json.dumps(web_content))

#         print(web_content)

        self.driver.close()
        return web_content

        # 教务处是tomcat, 没有配置304请求头


# def check_304_status_code(self, last_check_date):
#        header = {
#            "If-Modified-Since": arrow.get(last_check_date).year
#        }


if __name__ == "__main__":

    s = JwcSpider()
    t = s.crawl()
    print(t)

