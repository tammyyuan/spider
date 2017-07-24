#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/6 16:20
# File   : hrTencent.py

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
from hrqq.items import HrqqItem
from scrapy.linkextractors import LinkExtractor

class hrTencentSpider(CrawlSpider):
    name = 'hrqqspider'
    allowed_doamin = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?keywords=python&start=']
    rules = [
        Rule(LinkExtractor(allow=('start=\d+')),callback='parse_item',follow=True),
    ]

    def parse_item(self, response):
        for each in response.xpath('//tr[@class="even"] | //tr[@class="odd"]'):
            item = HrqqItem()
            item["job_name"] = each.xpath('.//a[@target="_blank"]/text()').extract()[0]
            item['job_class'] = each.xpath('./td[2]/text()').extract()[0] if len(each.xpath('./td[2]/text()').extract()) else ""
            item["job_num"] = each.xpath("./td[3]/text()").extract()[0]
            item["job_addr"] = each.xpath("./td[4]/text()").extract()[0]
            item["job_public"] = each.xpath("./td[5]/text()").extract()[0]

            yield item