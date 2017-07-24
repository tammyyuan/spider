# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuuserspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    answer_count = scrapy.Field()#回答数
    articles_count = scrapy.Field()#文章数量
    avatar_url = scrapy.Field()#头像url
    follower_count = scrapy.Field()#关注者人数
    gender = scrapy.Field()#性别
    headline = scrapy.Field()#个性签名
    url_token = scrapy.Field()#用户主页id
    user_id = scrapy.Field()#用户id
    name = scrapy.Field()#昵称
    business_name = scrapy.Field()#行业
    description = scrapy.Field()#个人简介
    educations_school = scrapy.Field()#学校
    # educations_major = scrapy.Field()#学院
    employments_company = scrapy.Field()#公司
    favorited_count = scrapy.Field()#获得收藏数
    voteup_count = scrapy.Field()#获得赞数
    following_count = scrapy.Field()#关注了人数
    locations_name = scrapy.Field()#现居地





