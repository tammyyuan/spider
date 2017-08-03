#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Myx
# Time   : 2017/7/28 18:55
# File   : KickstarterSpider.py

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from zhongchou.items import KickstarterItem
from scrapy import Request
from scrapy.spidermiddlewares.httperror import HttpError

class KickstarterSpider(CrawlSpider):
    name = 'kick'
    allowed_domains = ['kickstarter.com']
    start_urls = [
        # 'https://www.kickstarter.com',
        'https://www.kickstarter.com/discover?ref=nav',
        'https://www.kickstarter.com/projects/mobvoi/ticwatch-s-and-e-a-truly-optimized-smartwatch?ref=discover_index_popular',
    ]

    rules = [
        Rule(LinkExtractor(allow=(r'/discover.*', )), callback='parse_list', follow=True),
        # Rule(LinkExtractor(allow=(r'#',)), follow=True),
        Rule(LinkExtractor(allow=(r'/projects/.*', )), callback='parse_detail'),
    ]

    def parse_list(self, response):
        self.logger.info(response)

        grid_row = response.xpath('//div[@class="grid-row flex flex-wrap"]')
        if len(grid_row) > 0:
            for grid in grid_row:
                if len(grid.xpath('./div[@class="col-full col-sm-12-24 col-lg-8-24"]')) > 0:
                    for detail in grid.xpath('./div[@class="col-full col-sm-12-24 col-lg-8-24"]'):
                        data_project = detail.xpath('./div/@data-project').extract()[0]
                        data_project = data_project.replace('false', 'False')
                        data_project = data_project.replace('true', 'True')
                        data_project = data_project.replace('null', 'None')
                        data_project = eval(data_project)
                        if type(data_project) == dict:
                            url = data_project['urls']['web']['project']
                        else:
                            data_project = eval(data_project)
                            url = data_project['urls']['web']['project']
                        yield Request(url, callback=self.parse_detail, errback=self.parse_error)
                else:
                    for detail in grid.xpath('./div'):
                        data_project = detail.xpath('./@data-project').extract()[0]
                        data_project = data_project.replace('false', 'False')
                        data_project = data_project.replace('true', 'True')
                        data_project = data_project.replace('null', 'None')
                        data_project = eval(data_project)
                        if type(data_project) == dict:
                            url = data_project['urls']['web']['project']
                        else:
                            data_project = eval(data_project)
                            url = data_project['urls']['web']['project']
                        yield Request(url, callback=self.parse_detail, errback=self.parse_error)
    def parse_error(self, response):
        if isinstance(response.value, HttpError):
            pass

        yield
    def parse_detail(self, response):
        self.logger.info(response)
        item = KickstarterItem()

        item['item_id'] = response.url.split('/')[-1].split('?')[0]
        #众筹中
        if response.xpath('//div[@id="main_content"]/@class').extract()[0] == 'Campaign-state-live':

            item['title'] = response.xpath(
                '//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]/h2/text()').extract()[0].strip()
            item['des'] = response.xpath(
                '//div[@class="col-20-24 col-lg-15-24 hide block-md order-2-md"]/p/text()').extract()[0].strip()
            item['organizer'] = response.xpath(
                '//span[@class="navy-700 ml2 ml0-md"]/a/text()').extract()[0].strip()
            if len(response.xpath('div[@class="project-image mb2 cf aspect-ratio--object"]/div')) > 0:
                item['img_url'] = response.xpath(
                    '//div[@class="video-player"]/img/@src').extract()[0]
                item['video_url'] = response.xpath(
                    '//div[@class="video-player"]/video/source[1]/@src').extract()[0]
            else:
                try:
                    item['img_url'] = response.xpath(
                        '//div[@class="project-image mb2 cf aspect-ratio--object"]/div/img/@src').extract()[0]
                except:
                    item['img_url'] = response.xpath(
                        '//div[@class="project-image mb2 cf aspect-ratio--object"]/img/@src').extract()[0]
                item['video_url'] = ''


            item['raised_money'] = response.xpath(
                '//div[@class="col-md-8-24 block-lg hide"]/div/div[3]/div/span/text()').extract()[0]
            item['target_raise'] = response.xpath(
                '//div[@class="col-md-8-24 block-lg hide"]/div/div[3]/div/span[3]/span/text()').extract()[0]
            item['support_num'] = response.xpath(
                '//div[@class="col-md-8-24 block-lg hide"]/div/div[3]/div[2]/div/text()').extract()[0].strip()
            # item['last_days'] = response.xpath(
            #     '//div[@class="col-md-8-24 block-lg hide"]/div/div[3]/div[3]/div/span/text()').extract()[0]
            item['deadline'] = response.xpath(
                '//div[@class="col-md-8-24 block-lg hide"]/p/time/text()').extract()[0].strip()

            item['type'] = response.xpath(
                '//*[@id="content-wrap"]/section/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/a[1]/text()').extract()[
                0].strip()
            item['address'] = response.xpath(
                '//*[@id="content-wrap"]/section/div/div[1]/div[1]/div[2]/div/div/div/div/div/div/a[2]/text()').extract()[
                0].strip()

            item['status'] = '众筹中'

        else: # Campaign-state-successful
            item['status'] = '众筹结束'
            item['deadline'] = ' '

            item['title'] = response.xpath(
                '//*[@id="content-wrap"]/section/div[2]/div[1]/h2/span/a/text()').extract()[0]
            item['des'] = response.xpath(
                '//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[1]/div[2]/span/span/text()').extract()[0].strip()
            try:
                item['organizer'] = response.xpath(
                    '//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div[2]/div[1]/a/text()').extract()[0].strip()
            except:
                item['organizer'] = response.xpath(
                    '//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[2]/div[1]/a/text()').extract()[0].strip()

            if len(response.xpath('//*[@class="project-image mb2 cf aspect-ratio--object"]/div[@class="video-player"]')) > 0:
                item['img_url'] = response.xpath(
                    '//*[@id="video_pitch"]/img/@src').extract()[0]
                try:
                    item['video_url'] = response.xpath(
                        '//*[@id="video_pitch"]/video/source/@src').extract()[0]
                except:
                    item['video_url'] = response.xpath('./@data-video-url').extract()[0]
            else:
                item['img_url'] = response.xpath(
                    '//*[@id="content-wrap"]/section/div[2]/div[2]/div/div/div[1]/div/div/img/@src').extract()[0]
                item['video_url'] = ''
            try:
                item['raised_money'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/h3/span/text()').extract()[0]
                item['target_raise'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/span/text()').extract()[0]
                item['support_num'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/h3/text()').extract()[0].strip()
                item['type'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/a[2]/text()').extract()[0].strip()
                item['address'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div[2]/div[1]/div/div/a[1]/text()').extract()[0].strip()
            except:
                item['raised_money'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[2]/div[1]/h3/span/text()').extract()[0]
                item['target_raise'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[2]/div[1]/div/span/text()').extract()[0]
                item['support_num'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[2]/div[2]/h3/text()').extract()[0]
                item['type'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[1]/div/div/a[2]/text()').extract()[0].strip()
                item['address'] = response.xpath(
                    '//*[@id="content-wrap"]/div[2]/section[1]/div/div/div/div/div[1]/div[1]/div/div[1]/div/div/a[1]/text()').extract()[0].strip()

        self.logger.info('{}{}'.format(__name__, item))

        yield item


'''
{"id":940691311,
"photo":{"key":"assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif",
        "full":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=560&h=315&fit=crop&v=1501617486&auto=format&q=92&s=124f1681b3e96b38a60a7f7b41d3cc5a",
        "ed":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=352&h=198&fit=crop&v=1501617486&auto=format&q=92&s=66dfe87171b786ccdf0534aa91ccd850",
        "med":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=272&h=153&fit=crop&v=1501617486&auto=format&q=92&s=26ae21cf69ee135191a6449a235c34fd",
        "little":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=208&h=117&fit=crop&v=1501617486&auto=format&q=92&s=16252fc51625d151a0b8d3539f2196e1",
        "small":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=160&h=90&fit=crop&v=1501617486&auto=format&q=92&s=13ebe3d46eb812aa3b395217e7e1bd6b",
        "thumb":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=48&h=27&fit=crop&v=1501617486&auto=format&q=92&s=d44613d013349a47de90fd864cb2d8f8",
        "1024x576":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=1024&h=576&fit=crop&v=1501617486&auto=format&q=92&s=f3761810461bf1e28367dac540a81d58",
        "1536x864":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=1552&h=873&fit=crop&v=1501617486&auto=format&q=92&s=ec9fd6b16227fa617c4d9a252ab81174"},
    "name":"Enemy Kitchen by Michael Rakowitz at MCA Chicago",
    "blurb":"Bring this mobile food truck/art project to the MCA where U.S. veterans will serve free Iraqi dishes at community events.",
    "goal":30000.0,
    "pledged":3061.0,
    "state":"live",
    "slug":"enemy-kitchen-by-michael-rakowitz-at-mca-chicago",
    "disable_communication":false,
    "country":"US",
    "currency":"USD",
    "currency_symbol":"$",
    "currency_trailing_code":true,
    "deadline":1504220400,
    "state_changed_at":1501605381,
    "created_at":1500062911,
    "launched_at":1501605380,
    "staff_pick":true,
    "is_starrable":true,
    "backers_count":48,
    "static_usd_rate":1.0,
    "usd_pledged":"3061.0",
    "creator":{"id":801305394,
        "name":"Museum of Contemporary Art Chicago",
        "is_registered":true,
        "avatar":{"thumb":"https://ksr-ugc.imgix.net/assets/017/637/061/0a41375b387dd43ea3e48176ced447dc_original.jpg?w=40&h=40&fit=crop&v=1500927099&auto=format&q=92&s=6de447fac2a468699704f73896f4aca1",
                "small":"https://ksr-ugc.imgix.net/assets/017/637/061/0a41375b387dd43ea3e48176ced447dc_original.jpg?w=160&h=160&fit=crop&v=1500927099&auto=format&q=92&s=a232d80d614c710845b99f8629627b29",
                "medium":"https://ksr-ugc.imgix.net/assets/017/637/061/0a41375b387dd43ea3e48176ced447dc_original.jpg?w=160&h=160&fit=crop&v=1500927099&auto=format&q=92&s=a232d80d614c710845b99f8629627b29"},
                 "urls":{
                    "web":{"user":"https://www.kickstarter.com/profile/801305394"},
                    "api":{"user":"https://api.kickstarter.com/v1/users/801305394?signature=1501724505.d9d7c5903cc81e4c628035f5a882068b58b931da"}}},
    "location":{"id":2379574,
                "name":"Chicago",
                "slug":"chicago-il",
                "short_name":"Chicago, IL",
                "displayable_name":"Chicago, IL",
                "country":"US",
                "state":"IL",
                "type":"Town",
                "is_root":false,
                "urls":{"web":{"discover":"https://www.kickstarter.com/discover/places/chicago-il",
                                "location":"https://www.kickstarter.com/locations/chicago-il"},
                        "api":{"nearby_projects":"https://api.kickstarter.com/v1/discover?signature=1501707331.225ed4f1d2da85de5ab5a2825b26aaf296eba663&woe_id=2379574"}}},
    "category":{"id":1,
                "name":"Art",
                "slug":"art",
                "position":1,
                "color":16760235,
                "urls":{"web":{"discover":"http://www.kickstarter.com/discover/categories/art"}}},
    "profile":{"id":3073768,
                "project_id":3073768,
                "state":"inactive",
                "state_changed_at":1500062911,
                "name":null,
                "blurb":null,
                "background_color":null,
                "text_color":null,
                "link_background_color":null,
                "link_text_color":null,
                "link_text":null,
                "link_url":null,
                "show_feature_image":false,
                "background_image_opacity":0.8,
                "should_show_feature_image_section":true,
                "feature_image_attributes":{"image_urls":{"default":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=1552&h=873&fit=crop&v=1501617486&auto=format&q=92&s=ec9fd6b16227fa617c4d9a252ab81174",
                                                          "baseball_card":"https://ksr-ugc.imgix.net/assets/017/637/134/cde0d14ad16a374eb3ac24efb868e1af_original.tif?crop=faces&w=560&h=315&fit=crop&v=1501617486&auto=format&q=92&s=124f1681b3e96b38a60a7f7b41d3cc5a"}}},
    "spotlight":false,
    "urls":{"web":{"project":"https://www.kickstarter.com/projects/801305394/enemy-kitchen-by-michael-rakowitz-at-mca-chicago",
                    "rewards":"https://www.kickstarter.com/projects/801305394/enemy-kitchen-by-michael-rakowitz-at-mca-chicago/rewards"}},
    "percent_funded":10.203333333333333}
'''


