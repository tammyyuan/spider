#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Myx
# Time   : 2017/7/14 15:37
# File   : pandaSpider.py

import scrapy
from panda.items import PandaItem
from scrapy.spiders import Spider
from scrapy.http import Request
import json
import time, sys
from danmu import DanMuClient

# class DanmuSpider(object):
url = 'http://www.panda.tv/ajax_chatinfo?roomid=%s&_=%s'
rommid = 7000
dmc = DanMuClient(url % (str(rommid), str(int(time.time()))))
# dmc = DanMuClient('https://www.douyu.com/585704')
if not dmc.isValid(): print('Url not valid')

def pp(msg):
    print(msg.encode(sys.stdin.encoding, 'ignore').
        decode(sys.stdin.encoding))

@dmc.gift
def gift_fn(self, msg):
    self.pp('[%s] send a gift --%s' % (msg['Nickname'], msg['MsgType']))

@dmc.danmu
def danmu_fn(self, msg):
    self.pp('[%s] %s' % (msg['NickName'], msg['Content']))

@dmc.other
def other_fn(msg):
    pp('Other message received')

dmc.start(blockThread=True)




class pandaSpider(Spider):
    name = 'panda'

    page = 1

    headers = {
        ':authority': 'www.panda.tv',
        ':method': 'GET',
        ':path': '/live_lists?status=2&order=person_num&pageno=%s&pagenum=120' % str(page),
        ':scheme': 'https',
        'accept': 'text / html, application / xhtml + xml, application / xml;',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
        'cache-control': 'max - age = 0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }

    url = 'https://www.panda.tv/live_lists?status=2&order=person_num&pageno=%s&pagenum=120' % str(page)

    def start_requests(self):

        yield Request(self.url, headers=self.headers)

    def parse(self, response):
        item = PandaItem()

        dic = json.loads(response.text)
        print(dic)
        if dic['errno'] == 0:
            for room in dic['data']['items']:
                item['room_id'] = room['id']
                item['room_title'] = room['name']
                item['room_nickname'] = room['userinfo']['nickName']
                item['room_number'] = room['person_num']
                item['room_style'] = room['classification']['cname']
                yield item

            if self.page < (dic['data']['total'] // 120):
                time.sleep(5)
                self.page += 1
                print('page:', self.page)
                self.headers[':path'] = '/live_lists?status=2&order=person_num&pageno=%s&pagenum=120' % str(self.page)
                self.url = 'https://www.panda.tv/live_lists?status=2&order=person_num&pageno=%s&pagenum=120' % str(
                    self.page)
                yield Request(self.url, headers=self.headers)
        else:
            print('error:'+ dic['errmsg'])


