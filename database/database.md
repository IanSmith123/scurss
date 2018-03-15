数据库包含以下表：



python 操作postgresql数据库使用的[驱动](https://github.com/psycopg/psycopg2)


```bash
pip3 install psycopg2
pip3 install arrow
pip3 install lxml
pip3 install requests
```

操作数据库的几个函数
![](http://oqyjccf1n.bkt.clouddn.com/20171207-003453.png)

```
check_update()
```
首先需要初始化Update()一个实例，把当前获取的某一个网站的所有信息传给update对象，然后还要传入表的名字和数据库连接给他。

这个函数首先获取传入的self.table的这个表的所有的newsid,然后用来和当前传入的self.info这个json里面的每一条的newsid做集合，不存在于这个集合中的，那么就是教务处新公布的新闻，如果存在，那么获取这个新闻的newscontent字段的md5然后和self.info里面的对应的md5做比较，如果相同，那么判断教务处更新了新闻的内容。

更新的内容会放到self.update对象中，新公布的内容会放在self.new对象中，他们都是一个json串，

```
update_db_last_check_time()
```
该函数会在程序的插入数据库和更新数据库字段执行完成之后执行

直接设置每一个表的lastchecktime字段的值为当前的时间戳，传入的table是一个*kwags, 变长字符串，程序会对他进行遍历所有的新闻表进行设置


```
insert_new_news()
```
插入发生了刚公布的新闻，需要传入表名和新公布的的json内容和数据库连接

程序会对指定表明的数据库进行插入操作

### CreateDB.py
用于初始化数据库,每次执行程序都会执行一遍，如果不存在表的话会自动新建一个

但是程序连接到某个数据库，如果不存在的话，那么不会自动新建的
