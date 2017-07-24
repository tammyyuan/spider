# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HrqqItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    job_name = scrapy.Field()
    job_class = scrapy.Field()#职位类别
    job_num = scrapy.Field()#招聘人数
    job_addr = scrapy.Field() #地点
    job_public = scrapy.Field()#发布时间


    pass
