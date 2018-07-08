# -*- coding: utf-8 -*-
import scrapy
from demo.items import IpInfoItem


class IpproxySpider(scrapy.Spider):
    name = 'IpProxy'
    allowed_domains = ['xicidaili.com']
    start_urls = ['http://www.xicidaili.com/']

    def parse(self, response):
        tr = response.xpath('//*[@id="ip_list"]/tr')
        for i in tr:
            print('找到行数字={}'.format(i))
            ip_body = i.xpath('td/text()').extract()
            if len(ip_body) == 0:
                continue
            else:
                print('有效ip={}'.format(ip_body))
                ip_info = IpInfoItem()
                ip_info['ip'] = ip_body[0]
                ip_info['port'] = ip_body[1]
                ip_info['server_location'] =ip_body[2]
                ip_info['is_anonymity'] =ip_body[3]
                ip_info['type'] =ip_body[4]
                ip_info['time_to_live'] =ip_body[5]
                print("出现数据={}".format(ip_info))
                yield ip_info

