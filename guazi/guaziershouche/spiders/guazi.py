#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/24 09:17
# File   : guazi.py

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from guaziershouche.items import GuaziershoucheItem
from scrapy import Request


class GuaziErshouche(CrawlSpider):
    name = 'guazi'
    allowed_domains = ['guazi.com']
    start_urls = ['https://www.guazi.com/bj/buy/i7/', ]

    rules = [
        Rule(LinkExtractor(allow=(r"/\w+/buy/i7/$", ), deny=('/www/buy/.*', )), follow=True),
        Rule(LinkExtractor(allow=(r"/\w+/buy/o\d+i7/#bread$", ), deny=('/www/buy/.*', )), follow=True),
        Rule(LinkExtractor(allow=(r"/\w+/.{17}.htm$", )), callback='parse_detail')
    ]

    def parse_detail(self, response):
        print(response)
        print('parse_detail')
        item = GuaziershoucheItem()

        item['item_id'] = response.url.split('/')[-1].split('.')[0]

        item['title'] = response.xpath('/html/body/div[4]/div[3]/div[2]/div[1]/p/text()').extract()[0]
        item['price'] = response.xpath('/html/body/div[4]/div[3]/div[2]/div[2]/span[1]/text()').extract()[0]
        basic_info = {}
        for info in response.xpath('/html/body/div[4]/div[5]/ul/li'):
            value = info.xpath('./div/text()').extract()[0].strip()
            key = info.xpath('./text()').extract()[0].strip()
            if not key:
                key = '排放标准'
            basic_info[key] = value
        item['basic_info'] = basic_info

        basic_params = {}
        for i, params in enumerate(response.xpath('/html/body/div[4]/div[5]/div[2]/table[1]//tr')):
            if i != 0:
                key = params.xpath('./td[1]/text()').extract()[0].strip()
                value = params.xpath('./td[2]/text()').extract()[0].strip()
                basic_params[key] = value
        item['basic_params'] = basic_params


        yield item
