# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubanmovie250Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    movie_ranking = scrapy.Field()  # 排名
    movie_name = scrapy.Field()#电影名称
    movie_rating = scrapy.Field()#评分
    movie_ratnum = scrapy.Field()#p评分人数
    movie_imgurl = scrapy.Field()  # 图片地址

    image_urls = scrapy.Field()
    # image_paths = scrapy.Field()
    # images = scrapy.Field()




