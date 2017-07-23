# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from zhihuUserSpider import settings

class ZhihuuserspiderPipeline(object):

    #连接数据库
    def __init__(self):
        config = dict(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            use_unicode = False,
            cursorclass = pymysql.cursors.DictCursor,
            charset = 'utf8mb4'
        )
        print('连接数据库')
        self.connect = pymysql.connect(**config)
        self.cursor = self.connect.cursor()
        print('连接数据库成功')

    def process_item(self, item, spider):

        try:
            print("查询数据。。。")
            self.cursor.execute('select * from zhihuuser where user_id = %s', item['user_id'])
            res = self.cursor.fetchone()

            if res:
                print('更新数据...')
                self.cursor.execute('''update into zhihuuser(name,gender,answer_count,articles_count,follower_count,following_count,voteup_count,favorited_count,educations_school,employments_company,locations_name,headline,description,url_token,user_id,avatar_url) 
                                        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                                    (item['name'],item['gender'],item['answer_count'],item['articles_count'],
                                     item['follower_count'],item['following_count'],item['voteup_count'],item['favorited_count'],
                                     item['educations_school'],item['employments_company'],item['locations_name'],item['headline'],
                                     item['description'],item['url_token'],item['user_id'],item['avatar_url']))
            else:
                print('插入数据。。。')
                self.cursor.execute(
                    '''insert into zhihuuser(name,gender,answer_count,articles_count,follower_count,
                      following_count,voteup_count,favorited_count,educations_school,employments_company,
                      locations_name,headline,description,url_token,user_id,avatar_url) 
                      values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                    (item['name'], item['gender'], item['answer_count'], item['articles_count'],
                    item['follower_count'], item['following_count'], item['voteup_count'],
                    item['favorited_count'],item['educations_school'], item['employments_company'],
                    item['locations_name'],item['headline'],item['description'],
                    item['url_token'], item['user_id'], item['avatar_url']))
            print("数据库插入完成")
            self.connect.commit()
        except Exception as error:
            print("数据库插入错误: ",error)

        return item
