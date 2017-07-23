# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from pymongo import MongoClient

class PandaPipeline(object):

    def __init__(self):
        client = MongoClient('localhost',27017)
        self.db = client.panda
        self.collection = self.db.panda

    def process_item(self, item, spider):

        posts = self.db.posts
        try:
            posts.update_one(
                {'room_id':item['room_id']},
                {'$set': dict(item)},
                upsert=True,
            )
            print('插入数据成功')
        except Exception as error:
            print('插入数据错误：'+error)

        return item
