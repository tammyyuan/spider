#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/19 11:51
# File   : lianjiaSpider.py

import scrapy
from scrapy.spiders import Spider
from lianjia.items import LianjiaItem
from scrapy import Request


class LianjiaSpider(Spider):
    name = 'lianjia'
    Host = 'https://bj.lianjia.com'

    headers = {
        'Referer': 'https://bj.lianjia.com/zufang/rco10/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    url = 'https://bj.lianjia.com/zufang/rco10/'

    def start_requests(self):
        print('start')

        yield Request(url=self.url, headers=self.headers, callback=self.parse_home)
        # yield Request(url='https://bj.lianjia.com/zufang/haidian/rco10/',
        #               headers=self.headers,
        #               callback=self.parse_district)
        # yield Request(url='https://bj.lianjia.com/zufang/xierqi1/rco10/',
                      # headers=self.headers,
                      # callback=self.parse_xierqi)
        # yield Request(url='https://bj.lianjia.com/zufang/101101688504.html',
        #               headers=self.headers,
        #               callback=self.parse_house)

    def parse_home(self, response):
        print('home')
        print(response)

        option_list = response.xpath('//dd[@data-index="0"]/div[@class="option-list"]/a')
        for option in option_list[1:]:
            h = option.xpath('./text()').extract()[0]
            url =self.Host + option.xpath('./@href').extract()[0]
            yield Request(url=url, headers=self.headers, callback=self.parse_district)

    def parse_district(self, response):
        print('District')

        sublist = response.xpath('//div[@class="option-list sub-option-list"]/a')
        for area in sublist[1:]:
            h = area.xpath('./text()').extract()[0]
            url = self.Host + area.xpath('./@href').extract()[0]
            yield Request(url=url, headers=self.headers, callback=self.parse_xierqi)

    def parse_xierqi(self, response):
        print('xierqi')

        house_lsit = response.xpath('//ul[@class="house-lst"]/li')
        for house in house_lsit:
            title = house.xpath('./div[@class="info-panel"]/h2/a/text()').extract()[0]
            price = house.xpath('./div[@class="info-panel"]/div[2]/div/span/text()').extract()[0]
            l = house.xpath('./div[@class="info-panel"]/h2/a/@href').extract()[0]
            history = house.xpath('.//div[@class="con"]/text()').extract()[-1]
            refresh = house.xpath('.//div[@class="price-pre"]/text()').extract()[0]
            seed = house.xpath('.//div[@class="col-2"]/div/div/span[@class="num"]/text()').extract()[0]

            dic = dict(
                history=history,
                refresh=refresh,
                seed=seed,
            )
            # print(history, refrsh, seed)
            yield Request(url=l, headers=self.headers, meta={'his_item': dic}, callback=self.parse_house)


        #下一页
        page_data = response.xpath('//div[@class="page-box house-lst-page-box"]/@page-data').extract()[0]
        page_data = eval(page_data)
        'https://bj.lianjia.com/zufang/xierqi1/rco10/'
        if page_data['curPage'] < page_data['totalPage']:
            if 'pg' in response.url:
                response.url.replace(str(page_data['curPage']), str(page_data['curPage'] + 1))
            else:
                next_url = response.url[:-6] + 'pg' + str(page_data['curPage'] + 1) + 'rco10/'
            yield Request(url=next_url, headers= self.headers, callback=self.parse_xierqi)

    def parse_house(self, response):
        print('house')
        item = LianjiaItem()

        item['title'] = response.xpath('//div[@class="title"]/h1/text()').extract()[0]
        item['description'] = response.xpath('//div[@class="sub"]/text()').extract()[0]
        item['price'] = response.xpath('//span[@class="total"]/text()').extract()[0]
        item['area'] = response.xpath('//div[@class="zf-room"]/p[1]/text()').extract()[0]
        item['huxing'] = response.xpath('//div[@class="zf-room"]/p[2]/text()').extract()[0]
        item['louceng'] = response.xpath('//div[@class="zf-room"]/p[3]/text()').extract()[0]
        item['chaoxiang'] = response.xpath('//div[@class="zf-room"]/p[4]/text()').extract()[0]
        item['subway'] = response.xpath('//div[@class="zf-room"]/p[5]/text()').extract()[0]
        item['community'] = response.xpath('//div[@class="zf-room"]/p[6]/a/text()').extract()[0]
        localis = response.xpath('//div[@class="zf-room"]/p[7]/a/text()').extract()
        item['location'] = localis[0] + ' ' + localis[1]
        item['publish_time'] = response.xpath('//div[@class="zf-room"]/p[8]/text()').extract()[0]

        item['brokerName'] = response.xpath('//div[@class="brokerInfo"]/div/div/a/text()').extract()[0]
        phone = response.xpath('//div[@class="brokerInfo"]/div/div/text()').extract()
        item['brokerPhone'] = phone[-2].strip() + '转' + phone[-1].strip()
        img = response.xpath('//div[@class="brokerInfo"]/a/img/@src').extract()[0]
        item['brokerImg'] = img[:-12]

        item['houseNum'] = response.url.split('/')[-1][:-5]

        item['history'] = response.meta['his_item']['history']
        item['seedNum'] = response.meta['his_item']['seed']
        item['refresh'] = response.meta['his_item']['refresh']

        yield item





