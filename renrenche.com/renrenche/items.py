# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrencheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    carId = scrapy.Field()
    title = scrapy.Field()          # 标题
    img_urls = scrapy.Field()       # 图片
    price = scrapy.Field()          # 价格
    priceNew = scrapy.Field()       # 新车价格
    # service_charge = scrapy.Field() # 服务费
    summary = scrapy.Field()        # 上牌时间
    kilometre = scrapy.Field()      # 公里数
    fluid = scrapy.Field()          # 排放标准
    displacement = scrapy.Field()   # 排量
    licensed = scrapy.Field()       # 上牌城市
    high_points = scrapy.Field()    # 亮点
    test_report = scrapy.Field()    # 监测报告
    basic_params = scrapy.Field()   # 基本参数

    pass
