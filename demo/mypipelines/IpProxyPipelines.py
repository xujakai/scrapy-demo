# -*- coding: utf-8 -*-
import mysql.connector

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

class IpProxyPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='123456', database='crawler', )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        # print('保存数据了={}'.format(item))
        ip = item.get('ip')
        port = item.get('port')
        server_location = item.get('server_location')
        is_anonymity = item.get('is_anonymity')
        type = item.get('type')
        time_to_live = item.get('time_to_live')
        insert_sql = """
                    insert into ip_proxy(ip, port, server_location, is_anonymity, type,time_to_live)
                    VALUES (%s, %s, %s, %s,%s, %s);
                """
        self.cursor.execute(insert_sql, (ip, port, server_location, is_anonymity, type,time_to_live))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cursor.close()
        self.conn.close()
