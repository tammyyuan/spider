#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Myx
# Time   : 2017/7/9 15:48
# File   : lagouSpider.py

import scrapy
from scrapy.spiders import Spider
from lagou.items import LagouItem
from scrapy import Request
import json
import re


class LagouSpider(Spider):

    name = 'lagouspider'

    host = 'lagou.com'
    headers = {
        'Referer': 'https://www.lagou.com/jobs/list_Java?px=new&xl=%E6%9C%AC%E7%A7%91&city=%E5%8C%97%E4%BA%AC',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    list_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Cache-Control': 'max-age=0',
        'Referer': 'https://www.lagou.com/jobs/list_Java?px=new&xl=%E6%9C%AC%E7%A7%91&city=%E5%8C%97%E4%BA%AC',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': 'None',
        'X-Requested-With': 'XMLHttpRequest',
    }
    list_url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    pn = 1
    kd = 'Java'
    fromdata = {
        'first': 'true',
        'pn': str(pn),
        'kd': kd,
    }

    def start_requests(self):
        print('start-request')
        # yield Request('https://www.lagou.com/jobs/3247299.html', headers=self.headers,callback=self.job_parse)
        yield Request('https://www.lagou.com/', headers=self.headers, callback=self.home_parse)
        # yield scrapy.FormRequest(url=self.list_url,
        #                          formdata=self.fromdata,
        #                          meta={'formdata':self.fromdata},
        #                          headers=self.list_headers,
        #                          callback=self.list_parse)

    def home_parse(self, response):
        print('home_parse')
        try:
            for dl in response.xpath(
                    '//div[@class="mainNavs"]/div[1]/div[2]/dl')[:4]:
                for t in dl.xpath('./dd/a'):
                    # print(t.xpath('./text()').extract()[0])
                    kd = t.xpath('./text()').extract()[0]
                    url = 'https://www.lagou.com/jobs/positionAjax.json?px=new&city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
                    formdata = {
                        'first': 'true',
                        'pn': '1',
                        'kd': kd,
                    }
                    print(kd)
                    yield scrapy.FormRequest(url=url,
                                             formdata=formdata,
                                             headers=self.list_headers,
                                             meta={'formdata': formdata},
                                             callback=self.list_parse)
        except Exception as error:
            self.log('home_parse %s' % error)

    def list_parse(self, response):
        print('list_parse',response)
        try:
            dict = json.loads(response.text)

            print(dict['success'])
            print(response.meta['formdata']['kd'])
            if dict['success']:

                for job in dict['content']['positionResult']['result']:
                    job_id = job.get('positionId')
                    print(job_id)
                    job_url = 'https://www.lagou.com/jobs/' + str(job_id) + '.html'
                    yield Request(job_url,
                                  headers=self.headers,
                                  meta={'kd': response.meta['formdata']['kd']},
                                  callback=self.job_parse)

                formdata = response.meta['formdata']
                if len(dict['content']['positionResult']['result']) == 15:
                    print(formdata['pn'])
                    if int(formdata['pn']) < 30:
                        formdata['pn'] = str(int(formdata['pn']) + 1)
                        yield scrapy.FormRequest(url=self.list_url,
                                                 formdata=formdata,
                                                 meta={'formdata': formdata},
                                                 headers=self.list_headers,
                                                 callback=self.list_parse)
            else:
                print('list_parse false msg:', dict['msg'])
        except Exception as error:
            self.log('list_parse %s' % error)

    def job_parse(self, response):
        print('job response', response)
        item = LagouItem()

        try:
            item['kd'] = response.meta['kd']
            item['job_name'] = response.xpath(
                '//span[@class="name"]/text()').extract()[0]
            item['salary'] = response.xpath(
                '//dd[@class="job_request"]/p/span[1]/text()').extract()[0][:-1]
            item['city'] = response.xpath(
                '//dd[@class="job_request"]/p/span[2]/text()').extract()[0][1:-2]
            item['workYear'] = response.xpath(
                '//dd[@class="job_request"]/p/span[3]/text()').extract()[0][:-2]
            item['education'] = response.xpath(
                '//dd[@class="job_request"]/p/span[4]/text()').extract()[0][:-2]
            item['publish_time'] = response.xpath(
                '//dd[@class="job_request"]/p[2]/text()').extract()[0][:-8]
            item['advantage'] = response.xpath(
                '//dd[@class="job-advantage"]/p/text()').extract()[0]

            des = ''
            for str in response.xpath(
                    '//dd[@class="job_bt"]/div/p/text()').extract():
                str = str.strip()
                des += str
            item['description'] = des

            if len(response.xpath('//div[@class="work_addr"]/a')) == 4:
                try:
                    item['job_area'] = response.xpath(
                        '//div[@class="work_addr"]/a[3]/text()').extract()[0]
                except:
                    item['job_area'] = response.xpath(
                        '//div[@class="work_addr"]/text()').extract()[3].strip()[1:]
            elif len(response.xpath('//div[@class="work_addr"]/a')) == 1:
                item['job_area'] = response.xpath(
                    '//div[@class="work_addr"]/text()').extract()[0].strip()
            else:
                item['job_area'] = response.xpath(
                    '//div[@class="work_addr"]/text()').extract()[2].strip()[1:]
            item['company_name'] = response.xpath(
                '//h2[@class="fl"]/text()').extract()[0].strip()
            item['company_fullname'] = response.xpath(
                '//img[@class="b2"]/@alt').extract()[0]
            item['industryField'] = response.xpath(
                '//ul[@class="c_feature"]/li[1]/text()').extract()[1].strip()
            item['financeStage'] = response.xpath(
                '//ul[@class="c_feature"]/li[2]/text()').extract()[1].strip()
            item['companySize'] = response.xpath(
                '//ul[@class="c_feature"]/li[3]/text()').extract()[1].strip()

            url = response.url
            job_id = re.search(r'\d+',url).group()
            item['job_id'] = job_id

            yield item
        except Exception as error:
            self.log('job_parse + %s\n %s' % (response.url, error))
