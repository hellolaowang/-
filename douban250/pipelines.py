# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import copy

from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi


class Douban250Pipeline(object):
    # def process_item(self, item, spider):
    #     with open("result.txt", mode='a') as f:
    #         f.write(item['id'] + "," + item['rate'] + "," + item['title'] + "," + item['url'] + "\n")
    #     return item
    def __init__(self):
        self.douban_set = set()
        self.dbpool = adbapi.ConnectionPool(
            dbapiName='pymysql', host='localhost',
            db='database_name', user='username', passwd='password', charset='utf8', use_unicode=False)

    def process_item(self, item, spider):
        """
        利用集合原理去重
        :param item:
        :param spider:
        :return:
        """
        id = item['id']
        if id in self.douban_set:
            raise DropItem("Duplicate douban found:%s" % item)
        self.douban_set.add(id)
        asyn_item = copy.deepcopy(item)
        self.dbpool.runInteraction(self._conditional_insert, asyn_item)
        return item

    def _conditional_insert(self, tx, item):
        insert_sql = "insert into database_name.table_name(id, rate, title, url) values(%s,%s,%s,%s)"
        tx.execute(insert_sql, (item['id'], item['rate'], item['title'], item['url']))
        print("正在插入数据....")
        return item
