import requests
from lxml import etree
import arrow

web_list = {
    "jwc": "xx",
    "xsc": "xsc.edu.cn",
    "sf": "sf.scu.edu.cn"
}


class Spider(object):
    """
    所有爬虫的基类
    """

    def __init__(self):
        """
        web_title: string
        crawl_date: int, 保存时间戳便于处理
        """

        self.news_title = 'title'
        self.news_content = ''
        self.news_date = ''
        self.news_url = ''
        self.crawl_date = ''
        self.timestamp = ''

    def __str__(self):
        """
        :return:
        """
        print("web_title: ", self.web_title)
        print("web_crawl_date", self.crawl_date)



