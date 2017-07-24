# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class GuaziershouchePipeline(object):

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client.guaziershouche
        self.collection = self.db.guazi_collection

    def process_item(self, item, spider):

        try:
            self.collection.update_one(
                {'item_id': item['item_id']},
                {'$set': dict(item)},
                upsert=True,
            )
            print('数据插入成功')
        except Exception as e:
            print('数据插入错误error:%s \nitem:%s' % (e, item))
        return item
