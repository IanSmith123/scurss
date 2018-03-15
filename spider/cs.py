import json

import requests
import arrow
from lxml import etree

from spider.Spider import Spider

class CsSpider(Spider):
    def __init__(self):
        super().__init__()
        self.url = 'http://cs.scu.edu.cn/'

    def crawl(self):
        r = requests.get(self.url)
        r.encoding = 'gbk'
        tree = etree.HTML(r.text)
        news_titles = tree.xpath('//tbody//tbody//tbody/tr/td/a/text()')
        news_urls = tree.xpath('//tbody//tbody//tbody/tr/td/a/@href')
        news_date = tree.xpath('//tbody//tbody//tbody/tr/td[2]/div/text()')
        news_urls = ['http://cs.scu.edu.cn'+item for item in news_urls]

        # 把上面获取的到东西整理成一个json
        web_content = []
        for i, _ in enumerate(news_date):
            news_id = news_urls[i].split('/')[-1].split('.')[0]
            web_content.append(
                {
                    'id':news_id,
                    'title': news_titles[i],
                    'date': repr(arrow.get(news_date[i]).timestamp),
                    'url': news_urls[i],
                    'content': ''
                }
            )

        # 获取每一条新闻的具体内容
        for order, news in enumerate(web_content):
            r = requests.get(news['url'])
            r.encoding = 'gbk'
            tree = etree.HTML(r.text)
            content = tree.xpath('string(//*[@id="__01"]/tbody/tr[2]/td[1]/table[3])')
            # print(content)
            web_content[order]['content'] = content

#            print(r.text)

        # print(web_content)
        # with open('cs.json', 'w') as f:
         #    f.write(json.dumps(web_content))
        return web_content

