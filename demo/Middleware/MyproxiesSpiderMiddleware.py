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

