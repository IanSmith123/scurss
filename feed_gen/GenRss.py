import PyRSS2Gen
import arrow
import datetime
import psycopg2


class GenRss(object):
    # def __init__(self, conn):
    #         self.conn = conn

    def __init__(self):
        #self.pg = psycopg2.connect(host="108ed.les1ie.com", port='5432', database='scurss', user='postgres',
        #                           password='ms17010')

        self.pg = psycopg2.connect(host="pgsqldb", port='5432', database='scurss', user='postgres',
                                   password='ms17010')
        self.info = []

    def get_news_list(self):
        """
        三个新闻表中每个表中最新的十条新闻
        :return:
        """
        cur = self.pg.cursor()
        all_news = []
        for table in ['jwcnews', 'csnews', 'xscnews']:
            sql = """
            SELECT newstitle, newsurl, lastupdatetime from {} ORDER BY publishtime desc LIMIT 10;
        """.format(table)
            cur.execute(sql)
            for news in cur.fetchall():
                all_news.append({'title': news[0], 'url': news[1], 'lastupdatetime': news[2]})
        # print(all_news)
        # 组装成为文本
        self.info = all_news

    def gen_rss_sample(self):

        rss = PyRSS2Gen.RSS2(
            title="scurss feed",
            link="http://scurss.les1ie.com",
            description=" 四川大学校内新闻聚合平台",
            lastBuildDate=datetime.datetime.now(),
            items=[
                PyRSS2Gen.RSSItem(
                    title="jwc renew",
                    link="jwc.scu.edu.cn",
                    description="教务处的新闻更新",
                    # guid=PyRSS2Gen.Guid("http://jwc.scu.edu.cn/newsinfo/", "235.asp"),
                    pubDate=datetime.datetime(2017, 12, 9, 21, 2)
                ),
            ]
        )

        rss.write_xml(open("../web/deme.xml", "w"))
        print("generate success")

    def gen_rss(self):
        rss_item = []
        for news in self.info:
            # print(news)
            item = PyRSS2Gen.RSSItem(
                title=news['title'],
                link=news['url'],
                description=news['title'],
                pubDate=arrow.get(news['lastupdatetime']).format('YYYY-MM-DD')
            )
            rss_item.append(item)

        rss = PyRSS2Gen.RSS2(
            title="scurss feed",
            link="http://scurss.les1ie.com",
            description=" 四川大学校内新闻聚合平台",
            lastBuildDate=datetime.datetime.now(),
            items=rss_item
        )
        rss.write_xml(open("./web/feed.xml", "w"))
        # 修改格式
        f = open("./web/feed.xml", 'r')
        con = f.read()
        f.close()

        con = con.replace("iso-8859-1", 'utf-8')
        f = open('./web/feed.xml', 'w')
        f.write(con)
        f.close()



    def close_db(self):
        self.pg.close()


