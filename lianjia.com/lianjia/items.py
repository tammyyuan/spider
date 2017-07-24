# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaItem(scrapy.Item):

    title = scrapy.Field()          # 标题
    description = scrapy.Field()    # 详情
    price = scrapy.Field()          # 价格
    area = scrapy.Field()           # 面积
    huxing = scrapy.Field()         # 户型
    louceng = scrapy.Field()        # l楼层
    chaoxiang = scrapy.Field()      # 朝向
    subway = scrapy.Field()         # 地铁
    community = scrapy.Field()      # 小区
    location = scrapy.Field()       # 位置
    publish_time = scrapy.Field()   # 发布时间
    brokerName = scrapy.Field()     # 经纪人
    brokerImg = scrapy.Field()      # 经纪人头像
    brokerPhone = scrapy.Field()    # 联系方式
    houseNum = scrapy.Field()       # 链家编号
    history = scrapy.Field()        # 小区历史
    seedNum = scrapy.Field()        # 看过此房人数
    refresh = scrapy.Field()        # 刷新时间
