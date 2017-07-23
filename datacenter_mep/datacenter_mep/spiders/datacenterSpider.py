#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/18 23:08
# File   : datacenterSpider.py

import scrapy
from scrapy.spiders import Spider
from scrapy import FormRequest
import pandas
import json
import codecs
from pyquery import PyQuery as pq


class DatacenterSpider(Spider):
    name = 'dbspider'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'datacenter.mep.gov.cn:8099',
        'Origin': 'http://datacenter.mep.gov.cn:8099',
        'Referer': 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    url = 'http://datacenter.mep.gov.cn:8099/ths-report/report!list.action'

    formdata = {
        'page.pageNo': '1',
        'page.orderBy': '',
        'xmlname': '1462259560614',
        'queryflag': 'open',
        'gisDataJson': '',
        'isdesignpatterns': 'flase',
        'CITY': '北京',
        'V_DATE': '2010-07-01',
        'E_DATE': '2017-07-17',
    }

    def start_requests(self):

        yield FormRequest(url=self.url, callback=self.parse_aqi, method='POST', headers=self.headers, formdata=self.formdata)

    def parse_aqi(self, response):

        print(response)
        # doc = pq(response.text)
        # city_data = doc('td')
        # l = list(i.text() for i in city_data.items())
        # print(type(l))
        # print(l)

        data = pandas.read_html(response.text, attrs={'id': 'GridView1'})[0]
        data = data.drop([1, 5, 7], 1)
        data = data.drop([0])
        data.columns = ['序号', '城市', 'AQI', '首要污染物', '日期', '空气污染级别']
        # data.index = data['日期']
        data.sort_values(inplace=True, by='日期', ascending=False)
        print(data)
        # print(len(data.index))
        # print(dict(data.ix[1]))
        json_str = data.to_json(orient='records')
        # js = json.loads(json_str)
        #TODO 保存为utf8
        with codecs.open('data.json', 'w', encoding='utf8') as f:
            f.write(json_str)

        #下一页
        total = response.xpath('//div[@class="report_page"]/text()').extract()[0].strip()
        total_page = total.split('\n')[-1].strip()[5:]
        print(total_page)
        if int(self.formdata['page.pageNo']) == int(total_page):
            self.formdata['page.pageNo'] = str(int(self.formdata['page.pageNo']) + 1)
            yield FormRequest(
                url=self.url,
                callback=self.parse_aqi,
                method='POST',
                headers=self.headers,
                formdata=self.formdata)


        yield