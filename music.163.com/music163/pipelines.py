# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient
class Music163Pipeline(object):

    def __init__(self):
        client = MongoClient('127.0.0.1', 27017)
        self.db = client.music163
        self.collection = self.db.music163_collection

    def process_item(self, item, spider):
        posts = self.db.posts
        try:

            posts.update_one(
                {'commentId': item['commentId']},
                {'$set': dict(item)},
                upsert=True,
            )
            print('插入数据完成')
        except Exception as e:
            print('插入数据错误error:%s' % e)

        return item
