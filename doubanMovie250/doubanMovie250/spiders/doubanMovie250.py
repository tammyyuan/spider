#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/4 14:21
# File   : doubanMovie250.py
from scrapy import Request
from scrapy.spiders import Spider
from bs4 import BeautifulSoup
from doubanMovie250.items import Doubanmovie250Item

class DoubanMovieTop250(Spider):
    name = "doubanmovie250"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    doubanurl = "https://movie.douban.com/top250"
    image_urls = []
    def start_requests(self):
        yield Request(self.doubanurl,headers = self.headers)

    def parse(self, response):
        item = Doubanmovie250Item()
        print("response",response)
        soup = BeautifulSoup(response.body,"html5lib")
        # print("soup",soup.prettify())
        for tag in soup.find_all("div","item"):
            print("tag", tag.find("img").get("src"))
            print("tag", tag.find("span","rating_num").string)
            print("tag", tag.find_all("span")[-2].string)

            item['movie_name'] = tag.find("span").string
            item['movie_imgurl'] = tag.find("img").get("src")
            item['movie_rating'] = tag.find("span","rating_num").string
            item['movie_ratnum'] = tag.find_all("span")[-2].string[:-3] if tag.find_all("span")[-2].string else tag.find_all("span")[-1].string[:-3]
            item['movie_ranking'] = tag.find("em").string
            item["image_urls"] = [tag.find("img").get("src")]
            # print(item.movie_name,item.movie_ranking,item.movie_imgurl,item.movie_rating,item.movie_ratnum)
            yield item

        next_url = soup.find("link",rel = "next").get("href")
        print("next",next_url)
        if next_url :
            next_url = self.doubanurl + next_url

            yield Request(next_url,headers=self.headers)

