# -*- coding: utf-8 -*-
import scrapy
from Qiubai.items import QiubaiItem
from scrapy.http import Request


class QiubaiSpider(scrapy.Spider):
    name = 'qiubai'
    allowed_domains = ['qiushibaike.com']
    '''
    start_urls = ['http://qiushibaike.com/']
    '''
    def start_requests(self):
        ua={'user-agent':'Mozilla/5.0 (Linux; Android 7.0; STF-AL10 Build/HUAWEISTF-AL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/6.2 TBS/044006 Mobile Safari/537.36 V1_AND_SQ_7.5.0_794_YYB_D QQ/7.5.0.3430 NetType/4G WebP/0.3.0 Pixel/1080'}
        yield Request('http://qiushibaike.com/',headers=ua)

    def parse(self, response):
        item=QiubaiItem()
        item['name']=response.xpath('/html/head/title').extract()
        item['content']=response.xpath('/html/head/meta[7]').extract()
        yield item
        print("解析网页")
