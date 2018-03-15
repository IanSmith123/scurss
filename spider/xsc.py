import json

import requests
from lxml import etree
import arrow

class XscSpider():
    def __init__(self):
        self.url = 'http://xsc.scu.edu.cn/P/List/tzgg'
        self.url = 'http://xsc.scu.edu.cn/P/PartialArticle?id=43&menu=43&rn=1'

    def crawl(self):
        r = requests.get(self.url)
        tree = etree.HTML(r.text)
        # print(r.text)
        # news_url = tree.xpath("//div[@class='u-list-body']/ul/li/a/@href")
        # news_title = tree.xpath("//div[@class='u-list-body']/ul/li/a/text()")
        news_url = tree.xpath('/html/body/ul/li/a/@href')
        news_title = tree.xpath('/html/body/ul/li/a/text()')
        news_date = tree.xpath('/html/body/ul/li/span/text()')

        #  组装成一个json
        web_content = []
        for i, _ in enumerate(news_url):
            url = 'http://xsc.scu.edu.cn' + news_url[i]
            r = requests.get(url)
            tree = etree.HTML(r.text)
            content = tree.xpath('string(/html/body/section[2]/div[2])')

            news_id = news_url[i].split('/')[-1]
            web_content.append({'id': news_id, 'url': url, 'title': news_title[i], 'date': arrow.get(news_date[i]).timestamp, 'content': content})

        print("完成爬取学工部, 长度为", len(repr(web_content)))
        # with open('xsc.json', 'w') as f:
         #    f.write(json.dumps(web_content))
        return web_content




