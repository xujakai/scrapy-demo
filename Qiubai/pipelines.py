# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class QiubaiPipeline(object):
    def process_item(self, item, spider):
        print('有数据！！！！！！！！！')
        #print("提取到内容：{}={},类型{}".format(item['name'],item["contend"],type(item['name'])))
        for i in range(0,len(item['name'])):
            print("提取到内容：{}={}".format(item['name'][i],item['content'][i]))
        return item
