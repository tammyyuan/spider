# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class MongoPipeline(object):
    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client.lianjia
        self.collection = self.db.lianjian_collection

    def process_item(self, item, spider):
        posts = self.db.posts
        try:
            posts.update_one(
                {'houseNum': item['houseNum']},
                {'$set': dict(item)},
                upsert=True,
            )
            print('插入数据完成')
        except Exception as e:
            print('插入数据错误：%s' % e)

        return item


class LianjiaPipeline(object):
    def process_item(self, item, spider):
        return item
