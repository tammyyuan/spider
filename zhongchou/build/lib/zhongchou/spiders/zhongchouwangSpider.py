#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/27 20:08
# File   : zhongchouwangSpider.py

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Request
from zhongchou.items import ZhongchouWangItem


class ZhongchouwangSpider(CrawlSpider):
    name = 'zhongchouwang'

    allowed_domains = ['zhongchou.com']
    start_urls = [
        'http://www.zhongchou.com/',
        # 'http://www.zhongchou.com/deal-show/id-715823',
    ]

    rules = [
        # Rule(LinkExtractor(allow=(r'.*',)), follow=True),
        Rule(LinkExtractor(allow=(r'/browse/.*', )), follow=True),
        Rule(LinkExtractor(allow=(r'deal-show/id-\d+',)), callback='parse_detail')
    ]

    def parse_detail(self, response):
        self.logger.info(response)
        item = ZhongchouWangItem()

        try:
            item['item_id'] = response.url.split('/')[-1][3:]
            item['title'] = response.xpath(
                '//div[@class="jlxqh3_wai"]/h3/text()').extract()[0]
            item['organizer'] = response.xpath(
                '//div[@class="faqipeeson"]/span[2]/font/text()').extract()[0].strip()
            # item['des'] =
            item['img_url'] = response.xpath(
                '//div[@class="xqDetailBox"]/div/img/@data-src').extract()[0]
            item['raised_money'] = response.xpath(
                '//div[@class="xqDetailRight"]/div/div[2]/p/span/text()').extract()[0]
            item['support_num'] = response.xpath(
                '//div[@class="xqDetailRight"]/div/div/p/span/text()').extract()[0]
            item['raised_process'] = response.xpath(
                '//div[@class="xqDetailRight"]/div[2]/p/text()').extract()[0]
            item['last_days'] = response.xpath(
                '//div[@class="xqDetailRight"]/div[2]/div[2]/span/b/text()').extract()[0]
            item['target_raise'] = response.xpath(
                '//div[@class="xqDetailRight"]/div[2]/div[2]/span[2]/b/text()').extract()[0]
            item['type'] = response.xpath(
                '//div[@class="jlxqTitleText siteIlB_box"]/span/a/text()'
            ).extract()[0]
            item['commend_num'] = response.xpath(
                '//div[@class="xqInner clearfix"]/ul/li[3]/b/text()'
            ).extract()[0]
            addrs = response.xpath('//div[@class="jlxqTitleText siteIlB_box"]/span[2]/a')
            add_list = []
            for a in addrs:
                r = a.xpath('./text()').extract()[0].strip()
                add_list.append(r)
            item['address'] = ' '.join(add_list)
            tags = response.xpath('//div[@class="jlxqTitleText siteIlB_box"]/span[3]/a')
            tag_list = []
            for a in tags:
                t = a.xpath('./text()').extract()[0].strip()
                tag_list.append(t)
            item['tag'] = ' '.join(tag_list)

            status = response.xpath('//div[@class="mainIn02Box"]/div/div[2]/span/@class').extract()[0].strip()
            if status == 'xqStatusSpan zcz successed':
                item['status'] = '成功结束'
            elif status == 'xqStatusSpan zcz ordering':
                item['status'] = '众筹中'
            else:
                item['status'] = '其他'

            # 获取起始两个div节点的位置
            start = response.xpath('count(//div[@class="newXmxqBox"]/div[1]/preceding-sibling::*)+1').extract()[0]
            end = response.xpath('count(//div[@class="newXmxqBox"]/div[2]/preceding-sibling::*)+1').extract()[0]
            start = int(float(start))
            end = int(float(end))
            # 在两个div节点之间查找
            temp = []
            for i in range(start, end):
                if len(response.xpath('//div[@class="newXmxqBox"]/*[position()={}]/text()'.format(i)).extract()) > 0:
                    text = response.xpath(
                        '//div[@class="newXmxqBox"]/*[position()={}]/text()'.format(i)
                    ).extract()[0].strip()
                    temp.append(text)
            item['process_updating'] = '\n'.join(temp)

            yield item

            '''
    des = Field()               # 描述
    commend_num = Field()       # 评论数
    type = Field()              # 类别
    address = Field()           # 地址
    tag = Field()               # 标签'''
        except Exception as error:
            self.logger.error(error)
