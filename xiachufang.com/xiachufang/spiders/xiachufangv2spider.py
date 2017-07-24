#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/5 16:36
# File   : xiachufangv2spider.py

from scrapy.spiders import Spider
from xiachufang.items import XiachufangItem
from bs4 import BeautifulSoup
from scrapy import Request

class Xiachufangv2Spider(Spider):
    name = 'xiachufangv2'
    start_urls = ["https://www.xiachufang.com/explore/monthhonor/"]

    def parse(self, response):
        item = XiachufangItem()
        soup = BeautifulSoup(response.body,"html5lib")
        # print(soup.find_all("ul","list"))
        # print("len")
        # print(len(soup.find_all("div","normal-recipe-list honor-recipe-list")))
        for tag in soup.find("div","normal-recipe-list honor-recipe-list").find_all("li","pure-g"):
            # print(tag)
            # print("rank",tag.find("div").string.strip())
            # print("name",tag.find("img").get("alt"))
            # print("url",tag.find("img").get("data-src"))
            # print(tag.find("p","ing ellipsis").string)
            # print("sc",tag.find("span","score bold green-font").string)
            # print("num",tag.find("span","bold score"))
            item['rank'] = tag.find_all("div","recipe-list-order pure-u-1-12")[0].string.strip()
            item['name'] = tag.find("img").get("alt")
            item['url'] = tag.find("img").get("data-src")
            item['material'] = tag.find("p","ing ellipsis").string.strip()
            item['score'] = tag.find("span","score bold green-font").string
            item['mdNum'] = tag.find("span","bold score").string

            inx_ori = tag.find("img").get("data-src").rfind(".jpg")
            ori_url = tag.find("img").get("data-src")[:inx_ori+4]
            # print(ori_url)
            item['image_urls'] = [ori_url]

            yield item

        if soup.find("span","now").string != "下一页":
            if soup.find("a","next"):

                next_url = soup.find("a","next").get("href")
                next_url = "https://www.xiachufang.com" + next_url
                yield Request(next_url)