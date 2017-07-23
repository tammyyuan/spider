#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/19 18:03
# File   : wy163.py

import scrapy
from scrapy.spiders import Spider
from scrapy.http import Request, FormRequest
from Crypto.Cipher import AES
from music163.items import Music163Item
import base64
import json
import re
import codecs
import time
import random
import binascii


class Wy163(Spider):
    name = '163'

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'music.163.com',
        'Cookie': 'appver=1.5.0.75771;MUSIC_U=e954e2600e0c1ecfadbd06b365a3950f2fbcf4e9ffcf7e2733a8dda4202263671b4513c5c9ddb66f1b44c7a29488a6fff4ade6dff45127b3e9fc49f25c8de500d8f960110ee0022abf122d59fa1ed6a2;',
        'Origin': 'http://music.163.com',
        'Referer': 'http://music.163.com',
        # 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
    }
    url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_436016654?csrf_token='
    # url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_248475?csrf_token='


    formdata = dict(
        params='9umNdBqzUCyyPqDxKMVnPLPUcubI1YuF1gLd1JCzDeG1qvn3pqr5HeUbzAGABgVg9Sdo5ZCpj8VCToyRg/n4EVnIoe/k3pybzfp5W46gn4WymYZM2URUHdKTpN733k0aySDw2RVfYhEY9cyVP9zRgLMdDGtzemWMb2puvlJDLv57oTih38OgXSYYzRhsq+oc',
        encSecKey='19607698a9cccd2f9bfaa1e0078c4f6bdb3e52ac0bf08cab101d3ca3f4f4eb5c50ca897c47271c70fb355870cc3fe19aaef269084fc0b2b78fbee1a275467db68e9c3d418a28e09eedbc49ebc27018e85a54de7e53cfe4ea00e914da79a727ed4b6e3f805edc26c06d82287adc88bb318057c354e8c03c85a67bf398b7a94853',
    )

    first_param = "{rid:\"\", offset:\"0\", total:\"false\", limit:\"20\", csrf_token:\"\"}"
    second_param = "010001"
    third_param = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
    forth_param = "0CoJUm6Qyw8W8jud"

    def AES_encrypt(self, text, key):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(key, AES.MODE_CBC, "0102030405060708")
        encrypt_text = encryptor.encrypt(text)
        encrypt_text = base64.b64encode(encrypt_text).decode('utf-8')
        return encrypt_text

    def get_params(self, param):
        second_key = 16 * 'F'
        h_encText1 = self.AES_encrypt(param, self.forth_param)
        h_encText = self.AES_encrypt(h_encText1, second_key)
        return h_encText

    def get_encSecKey(self):
        text = 16 * 'F'
        text = text[::-1]
        # rs = int(text.encode('hex'), 16) ** int(self.second_param, 16) % int(self.third_param, 16)
        rs = int(codecs.encode(str.encode(text), 'hex_codec'), 16) ** int(self.second_param, 16) % int(self.third_param, 16)
        return format(rs, 'x').zfill(256)

    record_url = 'http://music.163.com/weapi/v1/play/record?csrf_token='
    # r_param = "{uid:\"\", offset:\"0\", total:\"false\", limit:\"100\", csrf_token:\"\", type:\"0\"}"
    r_param = "{uid:\"%d\", offset:\"0\", total:\"false\", limit:\"100\", csrf_token:\"\", type:\"0\"}"

    def start_requests(self):
        formdat = {
            'params': self.get_params(self.r_param % 81158988),
            'encSecKey': self.get_encSecKey(),
        }

        yield FormRequest(url=self.record_url, headers=self.headers, formdata=formdat, callback=self.parse_record)
        yield FormRequest(url=self.url, headers=self.headers, formdata=self.formdata, callback=self.parse_comment)

    def parse_record(self, response):
        print('record')

        # print('response: %s' % response.text)
        data = json.loads(response.text)
        if data['code'] == 200:
            crawl_times = 0
            for song in data['allData']:
                crawl_times += 1
                if crawl_times % 10 == 0:
                    time.sleep(3.14)
                # print(song['song']['name'])
                song_id = song['song']['id']
                song_name = song['song']['name']
                singer_name = ''
                for singer in song['song']['ar']:
                    singer_name = singer_name + singer['name']
                # print(singer_name)
                nameDic = dict(
                    singer_name=singer_name,
                    song_name=song_name,
                )
                # print(nameDic)
                self.url = 'http://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token='.format(song_id)
                yield FormRequest(url=self.url, headers=self.headers, formdata=self.formdata, meta={'nameDic': nameDic}, callback=self.parse_comment)

        else:
            print('parse_record data_code: %s %s' % (data['msg'],response.url))
            # print(response.text)

    def parse_comment(self, response):
        # print(response)
        item = Music163Item()

        #       --------   获赞数   ----------
        likedCount = 1
        try:
            data = json.loads(response.text)
            if data['code'] == 200:
                for comment in data['comments']:
                    if comment['likedCount'] >= likedCount:
                        item['time'] = comment['time']
                        item['likedCount'] = comment['likedCount']
                        item['content'] = comment['content']
                        item['commentId'] = comment['commentId']
                        item['avatarUrl'] = comment['user']['avatarUrl']
                        item['nickname'] = comment['user']['nickname']
                        item['userId'] = comment['user']['userId']
                        t = time.localtime(int(str(comment['time'])[:-3]))
                        item['time'] = time.strftime('%Y-%m-%d %H:%M', t)
                        item['songId'] = response.url.split('?')[0].split('/')[-1][7:]

                        item['song'] = response.meta.get('nameDic', {'': ''}).get('song_name', '漂洋过海来看你')
                        item['singer'] = response.meta.get('nameDic', {'': ''}).get('singer_name', '刘明湘')
                        # print(item)

                        yield item

                        try:
                            # TODO  uid
                            # record_param = "{uid:\"{}\", offset:\"0\", total:\"false\", limit:\"100\", csrf_token:\"\", type:\"0\"}".format(comment['user']['userId'])
                            record_data = {
                                'params': self.get_params(self.r_param % comment['user']['userId']),
                                'encSecKey': self.get_encSecKey(),
                            }
                            yield FormRequest(url=self.record_url, headers=self.headers, formdata=record_data,
                                              callback=self.parse_record)
                        except Exception as e:
                            print('comment to record error: %s' % e)

            else:
                print('parse_comment data_code:%s' % data['code'])
                print('parse_coment data:%s' % data)

            # 下一页
            hotcoments = [0, ]
            if 'hotComments' in data.keys():
                for com in data['hotComments']:
                    hotcoments.append(com['likedCount'])
            # print('\n\n\n' + str(max(hotcoments)) + '\n\n\n')
            # 如果 热评最高赞 小于 指定赞数 直接过 不再爬去
            if max(hotcoments) > likedCount:

                offset = re.search(r'"\d+"', self.first_param).group(0)[1:-1]
                if int(offset) + 20 < data['total']:
                    print('歌曲： %s' % response.meta.get('nameDic', {"": ""}).get('song_name', ''))
                    print('当前页%d 共%d页 -> 下一页' % ((int(offset) + 20) / 20, data['total']))
                    if ((int(offset) + 20) / 20) % 5 == 0:
                        print('sleep')
                        time.sleep(random.uniform(2, 10))
                        if ((int(offset) + 20) / 20) % 30 == 0:
                            time.sleep(random.uniform(2, 50))
                    offset = 'offset:"{}"'.format(int(offset) + 20)
                    old = re.search('offset:"\d+"', self.first_param).group(0)
                    self.first_param = self.first_param.replace(old, offset)
                    formdata = dict(
                        params=self.get_params(self.first_param),
                        encSecKey=self.get_encSecKey(),
                    )
                    yield FormRequest(url=self.url, method='POST', headers=self.headers, formdata=formdata,
                                      callback=self.parse_comment)

        except Exception as e:
            print('parse_comment error:%s' % e)
            print('response_url: %s' % response.url)
            print('response: %s' % response.text)
            # print('parse_comment :%s' % response.xpath('//span[@id="redir_msg"]/p/text()').extract()[0])



            # print(self.get_params())

            # rrid = response.url.split('?')[0].split('/')[-1]
            # offset = int(offset) + 20
            # print(rrid, offset)
            # f_param = '{"rid":\"\", "offset":\"{}\", "total":\"{}\", "limit":\"20\", "csrf_token":\"\"}'.format(offset, 'false')
            # self.first_param = f_param
            # print(self.first_param)


'''
            offset = re.search(r'\d+', self.first_param).group(0)
            if int(offset) + 20 < data['total']:
                print('下一页')
                # offset = r'offset:"{}"'.format(int(offset) + 20)
                # old = re.search(r'offset:"\d+"', self.first_param).group(0)
                # self.first_param = self.first_param.replace(old, offset)
                url = response.url
                print(url)
                rrid = url.split('?')[0].split('/')[-1][7:]
                offset = int(offset) + 20
                print(rrid, offset)
                param = "{rid:\"\", offset:\"{}\", total:\"{}\", limit:\"20\", csrf_token:\"\"}".format(offset, 'false')
                self.first_param = param
                print(self.first_param)
                formdata = dict(
                    params=self.get_params().decode('utf8'),
                    encSecKey=self.get_encSecKey(),
                )
                yield FormRequest(url=self.url, headers=self.headers, formdata=formdata, callback=self.parse_comment)




        # first_param = "{rid:\"\", offset:\"0\", total:\"true\", limit:\"20\", csrf_token:\"\"}"
        # offset = re.search(r'offset:"\d+"',self.first_param).group(0)
        offset = int(eval(self.first_param)['offset'])
        # print(eval(self.first_param))
        # offset = 1
        if offset >= 0:
        # if offset + 20 < data['total']:
            print('下一页')
            dic = dict(
                rid="",
                offset=str(offset + 20),
                total=False,
                limit='20',
                csrf_token="",
            )
            self.first_param = str(dic)
            # print(type(self.first_param))
            params = self.get_params().decode('utf8')
            print(params)
            formdata = dict(
                params=params,
                encSecKey=self.get_encSecKey(),
                # encSecKey='ae61d1b0be3794e4d1b9cb861694a7369c4a620afbfe3e80bbc6c0b7479cdf0ffd9219c8416c3ed5daba7cfa6c8848e64bd323e5fd1536f350f038fffeed1a92cf946832d98ca3c1cfc1c1a2a2c4a1930b4966209c107b36f32b804b95fee5b9d080b88c9b028cd5730e66033b7ea3701bca7d759f66d42cd9b42e8ec164ead7',
            )
            yield FormRequest(url=self.url, headers=self.headers, formdata=formdata, callback=self.parse_comment)
'''



