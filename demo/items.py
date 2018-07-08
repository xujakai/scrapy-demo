# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DemoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    publisher = scrapy.Field()
    ratings = scrapy.Field()
    edition_year = scrapy.Field()
    author = scrapy.Field()
    # 某本书的名字，作者，价格，评分等信息

class IpInfoItem(scrapy.Item):
    # define the fields for your item here like:

    # name = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
    server_location = scrapy.Field()
    is_anonymity = scrapy.Field()
    type = scrapy.Field()
    time_to_live = scrapy.Field()
    # 某本书的名字，作者，价格，评分等信息
    