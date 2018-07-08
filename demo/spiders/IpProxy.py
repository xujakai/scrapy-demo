# -*- coding: utf-8 -*-
import scrapy


class IpproxySpider(scrapy.Spider):
    name = 'IpProxy'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://xicidaili.com/']

    def parse(self, response):
        pass
