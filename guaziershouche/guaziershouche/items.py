# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziershoucheItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    price = scrapy.Field()
    basic_info = scrapy.Field()
    basic_params = scrapy.Field()
    item_id = scrapy.Field()

    pass
