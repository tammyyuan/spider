# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PandaItem(scrapy.Item):

    room_id = scrapy.Field()
    room_title = scrapy.Field()
    room_nickname = scrapy.Field()
    room_number = scrapy.Field()
    room_style = scrapy.Field()