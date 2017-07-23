# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163Item(scrapy.Item):

    likedCount = scrapy.Field()     # 赞数
    avatarUrl = scrapy.Field()      # 头像
    nickname = scrapy.Field()       # 昵称
    userId = scrapy.Field()         # 用户id
    content = scrapy.Field()        # 内容
    commentId = scrapy.Field()      # 评论id
    time = scrapy.Field()           # 时间
    song = scrapy.Field()           # 所属歌曲
    songId = scrapy.Field()         # 歌曲id
    singer = scrapy.Field()         # 歌手
