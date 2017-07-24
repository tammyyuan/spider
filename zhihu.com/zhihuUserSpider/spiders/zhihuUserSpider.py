#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/7 15:45

from scrapy.spiders import Spider
from zhihuUserSpider.items import ZhihuuserspiderItem
from scrapy import Request
import scrapy
import json

class ZhihuUserSpider(Spider):
    name = 'zhihuspider'
    allowed_domains = ['zhihu.com']
    #获取关注者参数
    include_follwees = 'data[*].answer_count,articles_count,gender,follower_count,is_followed,is_following,badge[?(type=best_answerer)].topics'
    #获取个人信息参数
    include_userInfo = 'locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics'

    follwees_url = 'https://www.zhihu.com/api/v4/members/{url_token}/followees?include={include_follwees}&offset={offset}&limit={limit}'
    # start_urls = []
    def start_requests(self):
        print('userinfo_url:::',self.get_userinfo_url())
        print('fllower_url:',self.get_fllowees_url())
        yield Request(self.get_userinfo_url(),callback=self.parse_userinfo)
        yield Request(self.get_fllowees_url(),callback=self.parse_follwees)

    def parse_userinfo(self, response):
        item = ZhihuuserspiderItem()
        data = json.loads(response.text)
        print('\nuser_info data：', data)
        for filed in item.fields:
            if filed in data.keys():
                item[filed] = data[filed]

        item['user_id'] = data['id']
        item['business_name'] = data['business']['name'] if data.get('business') else ' '

        if data.get('educations') :
            if 'school' in data.get('educations')[0].keys() and data.get('educations')[0].get('school'):
                item['educations_school'] = data.get('educations')[0].get('school').get('name')
        else:
            item['educations_school'] = ' '
        if data.get('employments'):
            if 'company' in data.get('employments')[0].keys() and data.get('employments')[0].get('company'):
                item['employments_company'] = data.get('employments')[0].get('company').get('name')
            else:
                item['employments_company'] = data.get('employments')[0].get('job').get('name')
        else:
            item['employments_company'] = ' '
        if data.get('locations'):
            item['locations_name'] = data.get('locations')[0].get('name')
        else:
            item['locations_name'] = ' '
        yield item
        yield Request(self.get_fllowees_url(url_token=data.get('url_token')),callback=self.parse_follwees)

    def parse_follwees(self, response):
        '''
        item = ZhihuuserspiderItem()
        print('response:\n')
        print(response)
        r_dict = json.loads(response.text)
        # data = r_dict['data']
        for info in r_dict['data']:
            item['avatar_url'] = info['avatar_url'][:-7] + '.jpg'
            item['answer_count'] = info['answer_count']
            item['url'] = info['url']
            item['url_token'] = info['url_token']
            item['id'] = info['id']
            item['articles_count'] = info['articles_count']
            item['name'] = info['name']
            item['headline'] = info['headline']
            item['gender'] = info['gender']
            item['follower_count'] = info['follower_count']

            yield item
        while not r_dict['is_end']:
            offset += 20
            try:
                yield Request(self.get_user_url(offset=offset))
        '''
        try:
            data = json.loads(response.text)
            try:
                if data.get('data'):
                    for user in data.get('data'):
                        url_token = user['url_token']
                        yield Request(self.get_userinfo_url(url_token=url_token),callback=self.parse_userinfo)
                if 'paging' in data.keys() and data.get('paging').get('is_end') == False:
                    yield Request(url=data.get('paging').get("next"), callback=self.parse_follwees)
            except Exception as error:
                print(error,'该用户没有url_token')
        except Exception as error:
            print(error,"该用户没有关注者")


    def get_fllowees_url(self, url_token = 'excited-vczh', offset = '0', limit = '20'):

        url = ('https://www.zhihu.com/api/v4/members/' + \
              url_token + \
              '/followees?' + \
              'include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics' + \
              '&offset=' + \
              offset + \
              '&limit=' + \
               limit)
        return url
    def get_userinfo_url(self,url_token= 'excited-vczh'):
        url = ('https://www.zhihu.com/api/v4/members/' + \
              url_token + \
              # '/followers?' + \
              '?include=locations,employments,gender,educations,business,voteup_count,thanked_Count,follower_count,following_count,cover_url,following_topic_count,following_question_count,following_favlists_count,following_columns_count,avatar_hue,answer_count,articles_count,pins_count,question_count,columns_count,commercial_question_count,favorite_count,favorited_count,logs_count,marked_answers_count,marked_answers_text,message_thread_token,account_status,is_active,is_bind_phone,is_force_renamed,is_bind_sina,is_privacy_protected,sina_weibo_url,sina_weibo_name,show_sina_weibo,is_blocking,is_blocked,is_following,is_followed,mutual_followees_count,vote_to_count,vote_from_count,thank_to_count,thank_from_count,thanked_count,description,hosted_live_count,participated_live_count,allow_message,industry_category,org_name,org_homepage,badge[?(type=best_answerer)].topics')
        return url