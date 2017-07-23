# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from lagou import settings
import logging

from pymongo import MongoClient
class LagouPipeline(object):

    def __init__(self):
        config = dict(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DB,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            use_unicode = False,
            cursorclass = pymysql.cursors.DictCursor,
            charset = 'utf8mb4'
        )
        self.connect = pymysql.connect(**config)
        self.cursor = self.connect.cursor()
        print('连接数据库')

    def process_item(self, item, spider):

        try:
            self.cursor.execute('select * from lagou where job_id = %s' , item['job_id'])
            res = self.cursor.fetchone()
            if res:
                print('更新数据')
                self.cursor.execute(
                    '''update into lagou(kd,job_name,salary,workYear,education,company_name,publish_time,
                    city,job_area,industryField,financeStage,companySize,company_fullname,job_id,advantage,
                    description) value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (item['kd'],item['job_name'],item['salary'],item['workYear'],item['education'],
                    item['company_name'],item['publish_time'],item['city'],item['job_area'],
                    item['industryField'],item['financeStage'],item['companySize'],
                    item['company_fullname'],item['job_id'],item['advantage'],item['description']))
            else:
                print("插入数据")
                self.cursor.execute(
                    '''insert into lagou(kd,job_name,salary,workYear,education,company_name,
                    publish_time,city,job_area,industryField,financeStage,companySize,
                    company_fullname,job_id,advantage,description) 
                    value (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (item['kd'],item['job_name'], item['salary'], item['workYear'], item['education'],
                    item['company_name'], item['publish_time'], item['city'], item['job_area'],
                    item['industryField'], item['financeStage'], item['companySize'],
                    item['company_fullname'], item['job_id'], item['advantage'], item['description']))
            self.connect.commit()
        except Exception as  error:
            print('插入数据错误：',error)
            logging.log(logging.ERROR, ('插入数据错误%s,\n%s' % (item,error)))


        return item

class MongoPipeline(object):
    print('mongo')
    def __init__(self):
        print('init')
        client = MongoClient("localhost",27017)
        self.db = client.lagou_database
        self.collection = self.db.lagou_collection

    def process_item(self, item, spider):
        print('process_item')
        posts = self.db.posts
        try:
            posts.update_one(
                {'job_id': item['job_id']},
                {'$set': dict(item)},
                upsert=True,
                )
            print('插入数据库成功')
        except Exception as error:
            logging("插入数据错误:%s,%s" % (error, item))

        return item

    # def close_spider(self, spider):
        # self.client.close()
