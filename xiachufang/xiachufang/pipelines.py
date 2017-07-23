# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy import Request
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from xiachufang import settings
import pymysql
import scrapy

#xiazai图片
class XiacfImagePipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        folder = request.meta.get("folder","aa")

        return '%s' % folder

    def get_media_requests(self, item, info):
        # folder = item['imger_urls'][0].split('/')[-1]
        folder = item['name'] + ".png"
        yield Request(item["image_urls"][0],meta={'folder':folder})

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not  image_paths:
            raise DropItem("Item contains no image")
        item['images'] = image_paths
        return item


#保存到数据库mysql
class XiachufangPipeline(object):

    def __init__(self):
        print("settings\n ss")
        print(type(settings.MYSQL_HOST))
        config = dict(
            host = settings.MYSQL_HOST,
            db = settings.MYSQL_DBNAME,
            user = settings.MYSQL_USER,
            password = settings.MYSQL_PASSWORD,
            charset = 'utf8mb4',
            use_unicode = False,
        )
        print("host:",settings.MYSQL_HOST)
        print(config)

        self.connect = pymysql.connect(**config)
        self.cursor = self.connect.cursor()

    # def _conditional_insert(self, item):
    #
    #     sql_insert = "insert into xiachufang(rank,name,score,maked_num,material,img_url) values (%s,%s,%s,%s,%s,%s)"
    #     sql_updata = "update into xiachufang(rank,name,score,maked_num,material,img_url) values (%s,%s,%s,%s,%s,%s)"
    #     params = (item['rank'],item['name'],item['score'],item['mdNum'],item['material',item['image_urls'][0]])
    #     print('done')
    #     self.cursor.execute('select * from xiachufang where rank = %s', item['rank'])
    #     res = self.cursor.fetchone()
    #     if res:
    #         self.cursor.execute(sql_updata,params)
    #         print("insert  update done")
    #     else:
    #         self.cursor.execute(sql_insert,params)
    #         print("insert done")

    def process_item(self, item, spider):

        try:
            print('to  insert')
            # self._conditional_insert(item=item)
            # sal_insert = '''insert into xiachufang(rank,name,score,make_num,material,img_url) values (%s,%s,%s,%s,%s,%s)'''
            # print(sal_insert)
            # sal_update = '''update into xiachufang(rank,name,score,make_num,material,img_url) values (%s,%s,%s,%s,%s,%s)'''
            # print(sal_update)
            # params = (item['rank'], item['name'], item['score'], item['mdNum'], item['material', item['image_urls'][0]])
            # print(params)

            print("topres")
            self.cursor.execute('select * from xiachufang where rank = %s', item['rank'])
            res = self.cursor.fetchone()
            print("downres:",res)
            if res:
                print("insert  update done")
                # self.cursor.execute(sal_update, params)
                self.cursor.execute('''update into xiachufang(rank,name,score,make_num,materials,img_url) 
                                        values (%s,%s,%s,%s,%s,%s)''',
                                    (item['rank'], item['name'], item['score'], item['mdNum'],
                                     item['material'], item['image_urls'][0]))
            else:
                print("inserting ...")
                # self.cursor.execute(sal_insert, params)
                self.cursor.execute('''insert into xiachufang(rank,name,score,make_num,materials,img_url) 
                                        values (%s,%s,%s,%s,%s,%s)''',
                                    (item['rank'], item['name'], item['score'], item['mdNum'],
                                     item['material'], item['image_urls'][0]))
                print('insert done')
            self.connect.commit()
        except Exception as error:
            print('errorin',error)
        # finally:
            # self.connect.close()
            # self.connect.commit()
        return item



