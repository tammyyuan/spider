# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class XiachufangItem(scrapy.Item):

    rank = scrapy.Field()#排名
    name = scrapy.Field()#名称
    url = scrapy.Field()#链接
    material = scrapy.Field()#材料
    score = scrapy.Field()#评分
    mdNum = scrapy.Field() #做过的人数
    image_urls = scrapy.Field()
    images = scrapy.Field()


