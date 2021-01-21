Description:
    利用scrapy框架爬取douban, 里边加入了一个集合的用法，通过使用集合，
    避免了将数据重复入库。

As Follows:
    1： scrapy startproject douban250
    2： cd douban250
    3:  scrapy genspider douban https://movie.douban.com/top250

Attention:
    1: 修改`pipelines.py`中的， host, username, password, database, table name,