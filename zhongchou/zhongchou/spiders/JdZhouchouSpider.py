#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Myx
# Time   : 2017/7/28 12:56
# File   : JdZhouchouSpider.py

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zhongchou.items import JdZhongchouItem
from scrapy.http import FormRequest
from zhongchou import settings
import random
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class JdZhouchouSpider(CrawlSpider):
    name = 'Jd'
    allowed_domains = ['z.jd.com']
    start_urls =[
        # 'https://z.jd.com/sceneIndex.html',
        'https://z.jd.com/bigger/search.html',
        # 'https://z.jd.com/project/details/85672.html',
    ]
    rules = [
        Rule(LinkExtractor(allow=r'/bigger/search.html',), callback='parse_list', follow=True),
        Rule(LinkExtractor(allow=r'/project/details/\d+.html$',), callback='parse_detail')
    ]

    def parse_error(self, failure):

        self.logger.error(repr(failure))
        if failure.check(HttpError):
            response = failure.value.response
            url = response.url
            self.logger.error('HttpError -- {}'.format(response.url))
        elif failure.check(DNSLookupError):
            request = failure.request
            url = request.url
            self.logger.error('DNSLookupError --- {}'.format(request.url))
        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            url = request.url
            self.logger.error('TimeoutError --- {}'.format(request.url))
        else:
            if not failure.request.url:
                url = failure.request.url
            else:
                url = failure.value.response.url

        with open('Jd_Traceback.txt', 'a') as f:
            f.write(url + '\n')


    # def start_requests(self):
    def parse_list(self, response):
        # log.msg(response)
        # self.logger.info(response)

        for item in response.xpath('//div[@class="l-result"]/ul/li'):
            item_url = item.xpath('./a[@class="link-pic"]/@href').extract()[0]
            item_url = 'https://z.jd.com' + item_url
            yield scrapy.Request(item_url, callback=self.parse_detail, errback=self.parse_error)

        user_agent = random.choice(settings.AGENTS)
        list_headers = {
            ':authority': 'z.jd.com',
            ':method': 'POST',
            ':path': '/bigger/search.html',
            ':scheme': 'https',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
            'accept-Encoding': 'gzip, deflate, br',
            'cache-control': 'max-age=0',
            'referer': 'https://z.jd.com/bigger/search.html',
            'upgrade-insecure-requests': '1',
            'user-agent': user_agent,
        }
        if 'categoryId' in response.url:
            categoryId = response.url.split('=')[1].split('&')[0]
        else:
            categoryId = ''

        total_item = response.xpath('//div[@class="l-statistics fr"]/strong/text()').extract()[0]
        max_page = (int(total_item) // 16) + 1
        for p in range(2, max_page):
            self.logger.info('第{}页---共{}页---categoryId:{}'.format(p, max_page, categoryId))
            formparams = {
                'status': '',
                'sort': 'zhtj',
                'categoryId': '',
                'parentCategoryId': '',
                'sceneEnd': '',
                'productEnd': '',
                'keyword': '',
                'page': str(p),
            }
            url = 'https://z.jd.com/bigger/search.html'
            yield FormRequest(url=url, formdata=formparams, headers=list_headers, callback=self.parse_list)

    def parse_detail(self, response):
        self.logger.info(response)
        item = JdZhongchouItem()
        try:
            item['item_id'] = response.url.split('/')[-1].split('.')[0]
            item['title'] = response.xpath('//div[@class="project-introduce"]/p/text()').extract()[0]
            try:
                status = response.xpath('//div[@class="project"]/div/i/@class').extract()[0]
            except:
                status = response.xpath('//div[@class=" project-old"]/div/i/@class').extract()[0]
            if status == 'zc-orange-preheat':
                item['status'] = '预热中'
            elif status == 'zc-success':
                item['status'] = '众筹成功'
            elif status == 'xm-success':
                item['status'] = '项目成功'
            elif status == 'zc-green-infinite':
                item['status'] = '筹 ∞'
            else:
                item['status'] = '众筹中'

            tags = response.xpath('//div[@class="tab-share-l"]/a/text()').extract()
            item['type'] = ' '.join(tags)
            item['img_url'] = response.xpath('//div[@class="project"]/div/img/@src').extract()[0][2:]

            symbol = response.xpath('//div[@class="project-introduce"]/p[3]/span/text()').extract()[0]
            mnum = response.xpath('//div[@class="project-introduce"]/p[3]/text()').extract()[0].strip()
            item['raised_money'] = symbol + mnum

            item['raised_process'] = response.xpath(
                '//div[@class="project-introduce"]/p[4]/span/text()').extract()[0].strip()[4:]
            item['support_num'] = response.xpath(
                '//div[@class="project-introduce"]/p[4]/span[2]/text()').extract()[0].strip()[:-4]
            # 筹 ∞项目
            if status == 'zc-green-infinite':
                item['target_raise'] = '∞'
                item['deadline'] = '∞'
            else:
                item['deadline'] = response.xpath('//p[@class="p-target"]/span/text()').extract()[0].strip()
                item['target_raise'] = symbol + response.xpath('//p[@class="p-target"]/span[2]/text()').extract()[
                    0].strip()
            item['organizer'] = response.xpath('//div[@class="promoters-name"]/a/span/text()').extract()[0].strip()
            item['company'] = response.xpath('//li[@class="clearfix contact-li"][1]/div[2]/text()').extract()[0]
            item['address'] = response.xpath('//li[@class="clearfix contact-li"][2]/div[2]/text()').extract()[0].strip()
            item['phone'] = response.xpath('//li[@class="clearfix contact-li"][3]/div[2]/text()').extract()[0]
        except Exception as e:
            self.logger.error(response.url, e)
            url = response.url
            with open('Jd_Traceback.txt', 'a') as f:
                f.write(url + '\n')

        self.logger.info(item)

        yield item
