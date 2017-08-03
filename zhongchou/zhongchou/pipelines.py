# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from zhongchou import settings
from zhongchou.items import ZhongchouWangItem, JdZhongchouItem, KickstarterItem
import logging

loger = logging.getLogger(__name__)

class ZhongchouPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DB,
            user=settings.MYSQL_USERNAME,
            password=settings.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True,
        )
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if isinstance(item, ZhongchouWangItem):
            create_table_sql = """\
                CREATE TABLE IF NOT EXISTS 众筹网 (\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                title VARCHAR(50),\
                organizer VARCHAR(25),\
                type VARCHAR(25),\
                status VARCHAR(25),\
                raised_money VARCHAR(25),\
                support_num VARCHAR(25),\
                raised_process VARCHAR(25),\
                last_days VARCHAR(25),\
                target_raise VARCHAR(25),\
                address VARCHAR(50),\
                tag VARCHAR(50),\
                item_id INT NOT NULL UNIQUE,\
                commend_num INT,\
                process_updating TEXT,\
                img_url VARCHAR(150)\
                )
            """
            update_table_sql = '''
            update 众筹网 set title = %s, organizer = %s, type = %s, status = %s, raised_money = %s,\
            support_num = %s,raised_process = %s,last_days = %s, target_raise = %s, address = %s,\
            tag = %s, item_id = %s, commend_num = %s, process_updating = %s, img_url = %s\
            where item_id = %s\
            '''
            insert_table_sql = '''
            insert into 众筹网 (title, organizer, type, status, raised_money, support_num,raised_process,\
            last_days, target_raise, address, tag, item_id, commend_num, process_updating, img_url)\
            value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\
            '''
            try:
                self.cursor.execute(create_table_sql)
                self.connect.commit()

                self.cursor.execute('select item_id from 众筹网 where item_id = %s', item['item_id'])
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(update_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['support_num'],
                                         item['raised_process'],
                                         item['last_days'],
                                         item['target_raise'],
                                         item['address'],
                                         item['tag'],
                                         item['item_id'],
                                         item['commend_num'],
                                         item['process_updating'],
                                         item['img_url'],
                                         item['item_id']))
                    # loger.info('数据库更新成功')
                    loger.info('众筹网    数据库更新成功')
                else:
                    self.cursor.execute(insert_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['support_num'],
                                         item['raised_process'],
                                         item['last_days'],
                                         item['target_raise'],
                                         item['address'],
                                         item['tag'],
                                         item['item_id'],
                                         item['commend_num'],
                                         item['process_updating'],
                                         item['img_url'],))
                    loger.info('众筹网    数据库插入成功')
                self.connect.commit()
            except Exception as error:
                loger.error('数据库错误: {}'.format(error))
            finally:
                # self.connect.close()
                pass

        elif isinstance(item, JdZhongchouItem):
            create_table_sql = """\
                        CREATE TABLE IF NOT EXISTS 京东众筹 (\
                        id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                        title VARCHAR(50),\
                        organizer VARCHAR(25),\
                        type VARCHAR(25),\
                        status VARCHAR(25),\
                        raised_money VARCHAR(25),\
                        raised_process VARCHAR(25),\
                        target_raise VARCHAR(25),\
                        support_num VARCHAR(25),\
                        deadline VARCHAR(25),\
                        item_id INT NOT NULL UNIQUE,\
                        company VARCHAR(50),\
                        address VARCHAR(50),\
                        phone VARCHAR(25),\
                        img_url VARCHAR(100)\
                        )
                        """
            update_table_sql = '''
                        update 京东众筹 set title = %s, organizer = %s, type = %s, status = %s, raised_money = %s,\
                        raised_process = %s,target_raise = %s,support_num = %s, deadline = %s, item_id = %s,\
                        company = %s, address = %s, phone = %s, img_url = %s\
                        where item_id = %s\
                        '''
            insert_table_sql = '''
                        insert into 京东众筹 (title, organizer, type, status, raised_money, raised_process,target_raise,\
                        support_num, deadline, item_id, company, address, phone, img_url)\
                        value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\
                        '''
            try:
                self.cursor.execute(create_table_sql)
                self.connect.commit()

                self.cursor.execute(
                    'select item_id from 京东众筹 where item_id=%s',
                    item['item_id'])
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(update_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['raised_process'],
                                         item['target_raise'],
                                         item['support_num'],
                                         item['deadline'],
                                         item['item_id'],
                                         item['company'],
                                         item['address'],
                                         item['phone'],
                                         item['img_url'],
                                         item['item_id']))
                    loger.info('JD 数据库更新成功')
                else:
                    self.cursor.execute(insert_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['raised_process'],
                                         item['target_raise'],
                                         item['support_num'],
                                         item['deadline'],
                                         item['item_id'],
                                         item['company'],
                                         item['address'],
                                         item['phone'],
                                         item['img_url']))
                    loger.info('JD 数据库插入成功')
                self.connect.commit()
            except Exception as error:
                loger.info('JD 数据库错误: {}'.format(error))

        elif isinstance(item, KickstarterItem):
            create_table_sql = """\
                CREATE TABLE IF NOT EXISTS Kickstarter (\
                id INT(11) AUTO_INCREMENT PRIMARY KEY,\
                title VARCHAR(100),\
                organizer VARCHAR(100),\
                type VARCHAR(25),\
                status VARCHAR(25),\
                raised_money VARCHAR(25),\
                target_raise VARCHAR(25),\
                support_num VARCHAR(25),\
                deadline VARCHAR(125),\
                item_id VARCHAR(125) NOT NULL UNIQUE,\
                address VARCHAR(75),\
                img_url VARCHAR(255),\
                video_url VARCHAR(255),\
                des TEXT\
                )
                """
            update_table_sql = '''
                                update Kickstarter set title = %s, organizer = %s, type = %s, status = %s,\
                                raised_money = %s, target_raise = %s, support_num = %s, deadline = %s,\
                                item_id = %s, address = %s, img_url = %s, video_url = %s, des = %s\
                                where item_id = %s\
                                '''
            insert_table_sql = '''
                                insert into Kickstarter (title, organizer, type, status, raised_money, target_raise,\
                                support_num, deadline, item_id, address, img_url, video_url, des)\
                                value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)\
                                '''
            try:
                self.cursor.execute(create_table_sql)
                self.connect.commit()

                self.cursor.execute(
                    'select item_id from Kickstarter where item_id = %s',
                    item['item_id'])
                result = self.cursor.fetchone()
                if result:
                    self.cursor.execute(update_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['target_raise'],
                                         item['support_num'],
                                         item['deadline'],
                                         item['item_id'],
                                         item['address'],
                                         item['img_url'],
                                         item['video_url'],
                                         item['des'],
                                         item['item_id']))
                    loger.info('Kick 更新数据库成功')
                else:
                    self.cursor.execute(insert_table_sql,
                                        (item['title'],
                                         item['organizer'],
                                         item['type'],
                                         item['status'],
                                         item['raised_money'],
                                         item['target_raise'],
                                         item['support_num'],
                                         item['deadline'],
                                         item['item_id'],
                                         item['address'],
                                         item['img_url'],
                                         item['video_url'],
                                         item['des'],))
                    loger.info('Kick 插入数据库成功')
                self.connect.commit()
            except Exception as error:
                loger.error('Kick 数据库错误: {}'.format(error))

        return item
