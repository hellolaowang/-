import scrapy

from douban250.items import Douban250Item


class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['https://movie.douban.com/top250']
    start_urls = [
        "https://movie.douban.com/j/search_subjects?type=movie&tag=冷门佳片&sort=recommend&page_limit=20&page_start="
        + str(x) for x in range(1, 50, 1)]

    def parse(self, response):
        rs = response.json()
        datas = rs.get('subjects')
        item = Douban250Item()
        for data in datas:
            item['title'] = data.get('title')
            item['rate'] = data.get('rate')
            item['url'] = data.get('url')
            item['id'] = data.get('id')
            yield item
