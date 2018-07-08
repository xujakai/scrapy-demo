# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class DemoPipeline(object):

    def __init__(self):
        pass

    def process_item(self, item, spider):
        print('保存数据了={}'.format(item))
        return item
