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
