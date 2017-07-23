#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/21 00:11
# File   : renrencheSpider.py

import scrapy
from scrapy.spiders import Spider
from scrapy import Request
import pandas as pd
import numpy as np
from renrenche.items import RenrencheItem

class RenrencheSpider(Spider):
    name = 'renrenche'

    url = 'https://www.renrenche.com/bj/ershouche/p3/?sort=publish_time&seq=desc&bc=gc'

    start_urls = [
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=r',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=m',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=h',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=f',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=d',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=qt',
        'https://www.renrenche.com/bj/ershouche/?sort=publish_time&seq=desc&bc=gc',
    ]

    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Cookie': 'Hm_lvt_c6fe62d8dab96f2dac708c242c0ede8f=1500565112; Hm_lpvt_c6fe62d8dab96f2dac708c242c0ede8f=1500567394; rrc_rrc_session=0clupd8hngob02ifhu8n04kof6; rrc_rrc_signed=s%2C0clupd8hngob02ifhu8n04kof6%2Ca3a542e7cee65186af4f50fc5b6eaab8; rrc_ip_city_twohour=bj; new_visitor_uuid=834977d46670ad7979787bb048cdce2b; visitor_flag=new; rrc_promo_two_years=rrc_promo_two_years; sigma-client-uuid=790985b7-4d02-45f2-8e29-8a2cb5a2083a; LXB_REFER=www.google.com; Hm_lvt_c6fe62d8dab96f2dac708c242c0ede8f=1500565112; Hm_lpvt_c6fe62d8dab96f2dac708c242c0ede8f=1500565386; isLoadPage=loaded; rrc_session_city=bj; _ga=GA1.2.448697011.1500565111; rls_uuid=C54FE004-5320-45E3-8378-7CF30356F3D7; _pzfxuvpc=1500565111497%7C2475684056129516993%7C12%7C1500567393970%7C1%7C%7C1559827739334854873; _pzfxsvpc=1559827739334854873%7C1500565111497%7C12%7Chttps%3A%2F%2Fwww.google.com%2F; Hm_lvt_c8b7b107a7384eb2ad1c1e2cf8c62dbe=1500565112; Hm_lpvt_c8b7b107a7384eb2ad1c1e2cf8c62dbe=1500567394; sigma-experiment={"bargain-style-exp":"test-b","exp-search-list":"group-a"}; rrc_ip_province=%E5%8C%97%E4%BA%AC; rrc_record_city=bj; rrc_fr=1350; rrc_ss=initiative',
        'Referer': 'https://www.renrenche.com/bj/ershouche/bc-d/?sort=publish_time&seq=desc',
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.headers, callback=self.parse_list)
        # yield Request(self.url, headers=self.headers, callback=self.parse_list)
        # yield Request('https://www.renrenche.com/bj/car/9aac55f6978f0933',
        #               headers=self.headers,
        #               callback=self.parse_detail)

    def parse_list(self, response):

        car_list = response.xpath('//ul[@class="row-fluid list-row js-car-list"]/li')

        for car in car_list:
            if car.xpath('./a/@class').extract()[0] == 'thumbnail':
                # title = car.xpath('./a/h3/text()').extract()[0].strip()
                # price = car.xpath('./a/div[@class="tags-box"]/div/text()').extract()[0].strip()
                # print(price, title)

                carId = car.xpath('./a/@data-car-id').extract()[0].strip()
                detail_url = 'https://www.renrenche.com/bj/car/{}'.format(carId)
                yield Request(detail_url, headers=self.headers, callback=self.parse_detail)

        current_page = response.xpath(
            '//ul[@class="pagination js-pagination"]/li[@class="active"]/a/text()').extract()[0].strip()
        l = len(response.xpath('//ul[@class="pagination js-pagination"]/li'))
        total_page = response.xpath(
            '//ul[@class="pagination js-pagination"]/li[{}]/a/text()'.format(l-1)).extract()[0].strip()
        print('当前页：%s, 共%s页' % (current_page, total_page))
        if int(current_page) < int(total_page):
            bc = response.url.split('&')[-1]
            next_url = 'https://www.renrenche.com/bj/ershouche/p{}/?sort=publish_time&seq=desc&{}'.format(str(int(current_page) + 1), bc)

            # next_url = '/bj/ershouche/bc-m/p{}/?sort=publish_time&seq=desc'.format(int(current_page) + 1)
            yield Request(next_url, headers=self.headers, callback=self.parse_list)


    def parse_detail(self, response):

        item = RenrencheItem()
        item['carId'] = response.url.split('/')[-1]
        item['title'] = response.xpath('//*[@class="title-name"]/text()').extract()[0]
        try:
            item['price'] = response.xpath('//*[@class="price detail-title-right-tagP"]/text()').extract()[0]
            item['priceNew'] = response.xpath('//*[@class="new-car-price detail-title-right-tagP"]/span/text()').extract()[0]
            # item['service_charge'] = response.xpath('//*[@id="js-service-wrapper"]/div[1]/p[2]/strong/text()').extract()[0]
            item['summary'] = response.xpath(
                '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[1]/div/p/strong/text()').extract()[0]
            item['kilometre'] = response.xpath(
                '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[2]/div/p/strong/text()').extract()[0]
            item['fluid'] = response.xpath(
                '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[3]/div/p/strong/text()').extract()[0]

            if len(response.xpath('//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li')) == 5:
                item['displacement'] = response.xpath(
                    '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[4]/div/strong/text()').extract()[0]
                item['licensed'] = response.xpath(
                    '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[5]/div/strong/@licensed-city').extract()[0]
            else:
                item['displacement'] = ''
                item['licensed'] = response.xpath(
                    '//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li[4]/div/strong/@licensed-city').extract()[0]

                img_urls = []
                imgs = response.xpath('//ul[@class="slides gallery-img"]/li')
                for img in imgs:
                    img_url = img.xpath('./div/img/@src').extract()[0].strip()
                    img_url = img_url.split('?')[0][2:]
                    img_urls.append(img_url)
                item['img_urls'] = img_urls

                # 亮点
                high_points = []
                liangdian = response.xpath('//*[@id="js_load_merti_data"]/span')
                for ld in liangdian:
                    h = ld.xpath('./text()').extract()[0]
                    high_points.append(h)
                item['high_points'] = high_points
        except:
            if len(response.xpath('//*[@id="basic"]/div[3]/div/div/div[1]/p')) > 1:
                item['price'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/p[2]/text()').extract()[0]
            else:
                item['price'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/p[2]/text()').extract()[0]
            if len(response.xpath('//*[@id="basic"]/div[3]/div/div/div[2]/ul/li')) > 1:
                item['priceNew'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/ul/li[2]/text()').extract()[0]
            else:
                item['priceNew'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/ul/li/text()').extract()[0]
            item['summary'] = response.xpath(
                '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[1]/p/strong/text()').extract()[0]
            item['kilometre'] = response.xpath(
                '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[2]/p/strong/text()').extract()[0]
            item['fluid'] = response.xpath(
                '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[3]/p/strong/text()').extract()[0]

            if len(response.xpath('//ul[@class="row-fluid list-unstyled box-list-primary-detail"]/li')) == 5:
                item['displacement'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[4]/p/strong/text()').extract()[0]
                item['licensed'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[5]/p/strong/@licensed-city').extract()[0]
            else:
                item['displacement'] = ''
                item['licensed'] = response.xpath(
                    '//*[@id="basic"]/div[3]/div/div/div[@class="detail-box"]/div[2]/ul/li[4]/div/strong/@licensed-city').extract()[0]
            img_urls = []
            '//*[@id="slider"]/div/div/div[1]'
            '//*[@id="slider"]/div/div/div[1]/div/img'
            imgs = response.xpath('//div[@id="sliderModal"]//div[@id="slider"]/div')
            for img in imgs:
                try:
                    img_url = img.xpath('./img/@data-src').extract()[0].strip()
                except:
                    img_url = img.xpath('./img/@src').extract()[0].strip()
                img_url = img_url.split('?')[0][2:]
                img_urls.append(img_url)
            item['img_urls'] = img_urls
            item['high_points'] = []

        #监测报告
        test_title = []
        for t in response.xpath('//div[@id="report"]/div/div/p/span'):
            test_title.append(t.xpath('./text()').extract()[0].strip())
        test_content = {}
        key1, value1 = '', ''
        for tr in response.xpath('//div[@id="report"]/div/div/div/table//tr'):
            for i, td in enumerate(tr.xpath('./td')):
                if len(td.xpath('./text()').extract()) > 0:
                    if (i % 2) == 0:
                        key1 = td.xpath('./text()').extract()[0].strip()
                    else:
                        value1 = td.xpath('./text()').extract()[0].strip()
                    test_content.update({key1: value1})
        item['test_report'] = {
            'title': test_title,
            'content': test_content,
        }

        #基本参数
        basic_params = {}
        key2, value2 = '', ''
        for j, tr in enumerate(response.xpath('//table[@id="basic-parms"]//tr')):
            if j != 0:
                for td in tr.xpath('./td'):
                    # print(len(td.xpath('./*')))
                    if len(td.xpath('./*')) > 0:
                        key2 = td.xpath('./div[1]/text()').extract()[0].strip()
                        value2 = td.xpath('./div[2]/text()').extract()[0].strip()
                        basic_params.update({key2: value2})
        item['basic_params'] = basic_params


        yield item









