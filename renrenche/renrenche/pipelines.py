# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class RenrenchePipeline(object):

    def __init__(self):
        cli = MongoClient('127.0.0.1', 27017)
        self.db = cli.renrenche
        self.collection = self.db.renrenche

    def process_item(self, item, spider):
        posts = self.db.renrenche
        try:
            posts.update_one(
                {'carId': item['carId']},
                {'$set': dict(item)},
                upsert=True
            )
            print('插入数据')
        except Exception as e:
            print('插入数据错误%s' % e)
        return item


