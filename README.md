# scrapy-demo
爬虫框架scrapy的示例代码
本示例爬取代码为豆瓣图书榜单上的数据信息

## 一、项目构建
在命令行下操作
### 1.1 创建工程
```bash
scrapy startproject scrapy-demo
```
### 1.2 创建爬虫程序
进入scrapy-demo目录下
```bash
scrapy genspider douban douban.com
```

## 二、基本结构

    scrapy.cfg  项目的配置信息，主要为Scrapy命令行工具提供一个基础的配置信息。（真正爬虫相关的配置信息在settings.py文件中）
    items.py    设置数据存储模板，用于结构化数据，如：Django的Model
    pipelines    数据处理行为，如：一般结构化的数据持久化
    settings.py 配置文件，如：递归的层数、并发数，延迟下载等
    spiders      爬虫目录，如：创建文件，编写爬虫规则


## 三、运行
进入项目目录下运行
```bash
直接运行 scrapy crawl douban
```
    或将数据存为csv scrapy crawl douban -o bookInfo.csv
## 四、items数据存储模板

```python
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
```

## 五、pipelines数据处理行为
使用MySQL做数据持久化
```python
# -*- coding: utf-8 -*-
import mysql.connector
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class DemoPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='123456', database='crawler', )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # print('保存数据了={}'.format(item))
        name = item.get('name')
        price = item.get('price')
        publisher = item.get('publisher')
        ratings = item.get('ratings')
        edition_year = item.get('edition_year')
        author = item.get('author')
        insert_sql = """
                    insert into book(name, price, publisher, ratings, edition_year,author)
                    VALUES (%s, %s, %s, %s,%s, %s);
                """
        self.cursor.execute(insert_sql, (name, price, publisher, ratings, edition_year,author))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()

```

## 六、Spider爬虫目录文件
*注意：一般创建爬虫文件时，以网站域名命名*

```python
import scrapy
from demo.items import DemoItem


class DoubanDemoSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/top250']

    def parse(self, response):
        yield scrapy.Request(response.url, callback=self.parse_page)

        for page in response.xpath('//div[@class="paginator"]/a'):
            link = page.xpath('@href').extract()[0]
            yield scrapy.Request(link, callback=self.parse_page)

    def parse_page(self, response):
        for item in response.xpath('//tr[@class="item"]'):
            book = DemoItem()
            book['name'] = item.xpath('td[2]/div[1]/a/@title').extract()[0]
            book['ratings'] = item.xpath('td[2]/div[2]/span[@class="rating_nums"]/text()').extract()[0]
            # book['ratings'] = item.xpath('td[2]/div[2]/span[2]/text()').extract()[0]
            book_info = item.xpath('td[2]/p[1]/text()').extract()[0]
            book_info_contents = book_info.strip().split(' / ')
            book['author'] = book_info_contents[0]
            book['publisher'] = book_info_contents[1]
            book['edition_year'] = book_info_contents[2]
            book['price'] = book_info_contents[3]
            yield book
```

## 七、settings.py配置信息

### 7.1 添加请求头
```python
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
```
### 7.2 启用pipelines
指定豆瓣书籍信息存数方式
```python
# 指定了豆瓣网的数据存储方式
ITEM_PIPELINES = {
    'demo.pipelines.DemoPipeline': 300,
}
```
指定ip存储方式
```python
# ITEM_PIPELINES = {
#     'demo.pipelines.DemoPipeline': 300,
# }
ITEM_PIPELINES = {
    'demo.pipelines.DemoPipeline': 300,
    'demo.mypipelines.IpProxyPipelines.IpProxyPipeline': 300,
 }
```
### 7.3 是否遵照爬虫协议(修改为false或删除)
```python
ROBOTSTXT_OBEY = False
```
## 八、添加动态代理池
### 8.1 编写设置代理ip文件
创建demo/Middleware/MyproxiesSpiderMiddleware.py
```python
# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import mysql.connector
import random
import time
from demo.utils.LoadIpUtil import LoadIpUtils
from scrapy import signals
# from demo.settings import IPPOOL # 将代理IP写死在ippoll中
import scrapy
from scrapy import log

class ProxyMiddleWare(object):
    """docstring for ProxyMiddleWare"""
    def __init__(self):
        # 从数据库中加载代理ip
        self.ips = LoadIpUtils.loadIp()
        print('所有可用的ip{}：{}'.format(len(self.ips), self.ips))

    def process_request(self, request, spider):
        '''对request对象加上proxy'''
        proxy = self.get_random_proxy()
        print("this is request ip:" + proxy)
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        # print('========================本次响应状态码=={}============='.format(response.status))
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        '''随机从文件中读取proxy'''
        proxy = random.choice(self.ips).strip()
        '''
        while 1:
            with open('E:\GitHub-clone\scrapy-demo\ip.txt', 'r') as f:
                proxies = f.readlines()
            if proxies:
                break
            else:
                time.sleep(1)
        proxy = random.choice(proxies).strip()
        '''
        return proxy
```
### 8.2 读取ip工具包（从本地数据库读取）
```python

import mysql.connector

class LoadIpUtils:

    @staticmethod
    def loadIp():
        conn = mysql.connector.connect(user='root', password='123456', database='crawler', )
        cursor = conn.cursor()
        query_sql = """
                select type,ip,port from ip_proxy where is_valid=1;
                """
        cursor.execute(query_sql)
        list = []
        for type, ip, port in cursor:
            list.append('{}://{}:{}'.format(type, ip, port))
        cursor.close()
        conn.close()
        # print(list)
        return list
```

### 8.3 修改setting文件
```python
DOWNLOADER_MIDDLEWARES = {
#    'myproxies.middlewares.MyCustomDownloaderMiddleware': 543,
     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware':None,
     'demo.Middleware.MyproxiesSpiderMiddleware.ProxyMiddleWare':125,
     'scrapy.downloadermiddlewares.defaultheaders.DefaultHeadersMiddleware':None
}
```

### 8.4 可以设置超时管理
```python
# DOWNLOAD_TIMEOUT = 300
```