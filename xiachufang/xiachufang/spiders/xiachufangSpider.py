#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/5 14:55
# File   : xiachufangSpider.py

from scrapy.spiders import Spider
from xiachufang.items import XiachufangItem
from scrapy.contrib.loader import ItemLoader,Identity
from scrapy.selector import Selector

class XiachuafangSpider(Spider):
    name = "xiachufangSpider1"
    allowed_domains = ["xiachufang.com"]
    start_urls = ["https://www.xiachufang.com/explore/monthhonor/"]

    def parse(self, response):

        item = XiachufangItem()
        # con_lis = response.xpath("//ul[@claa='list']/li").extract()
        print()
        # print(con_lis)

        sel = Selector(response)
        con_lis = sel.xpath("//ul[@claa='list']/li").extract()
        print(con_lis)
        for content in con_lis :
            l = ItemLoader(item=XiachufangItem(), response=response)
            print(content.xpath(".//div[@class='pure-g']/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[0]/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='cover pure-u']/@src").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[1]/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[2]/spa[0]/text()").extract()[0])




        for content in con_lis:
            print(content.xpath(".//div[@class='pure-g']/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[0]/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='cover pure-u']/@src").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[1]/text()").extract()[0])
            print(content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[2]/spa[0]/text()").extract()[0])
            item['rank'] = content.xpath(".//div[@class='pure-g']/text()").extract()[0]
            item['name'] = content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[0]/text()").extract()[0]
            item['url'] = content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='cover pure-u']/@src").extract()[0]
            item['material'] = content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[1]/text()").extract()[0]
            item['score'] = content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[2]/spa[0]/text()").extract()[0]
            item['mdNum'] = content.xpath(".//div[@class='pure-u-11-12']/a/div[@class='info pure-u']/p[2]/span[1]/text()").extract()[0]

            yield item


