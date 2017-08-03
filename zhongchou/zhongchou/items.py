# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class ZhongchouWangItem(scrapy.Item):

    title = Field()             # 标题
    organizer = Field()         # 组织者
    # des = Field()               # 描述
    img_url = Field()           # 图片url
    raised_money = Field()      # 已筹款
    support_num = Field()       # 支持数
    raised_process = Field()    # 筹款进度
    last_days = Field()         # 剩余天数
    target_raise = Field()      # 目标集资
    commend_num = Field()       # 评论数
    type = Field()              # 类别
    address = Field()           # 地址
    tag = Field()               # 标签
    process_updating = Field()  # 项目简介
    item_id = Field()           # id
    status = Field()            # 众筹状态


class JdZhongchouItem(scrapy.Item):

    title = Field()             # 标题
    status = Field()            # 众筹状态
    type = Field()              # 类别
    img_url = Field()           # 图片url
    raised_money = Field()      # 已筹款
    raised_process = Field()    # 筹款进度
    target_raise = Field()      # 目标集资
    support_num = Field()       # 支持数
    # last_days = Field()         # 剩余天数
    deadline = Field()          # 截止日期
    organizer = Field()         # 项目发起人
    company = Field()           # 公司名称
    address = Field()           # 地址
    phone = Field()             # 联系方式
    item_id = Field()           # id

class KickstarterItem(scrapy.Item):

    title = Field()             # 标题
    status = Field()            # 众筹状态
    type = Field()              # 类别
    img_url = Field()           # 图片url
    video_url = Field()         # 视频url
    raised_money = Field()      # 已筹款
    target_raise = Field()      # 目标集资
    support_num = Field()       # 支持数
    last_days = Field()         # 已筹款天数
    deadline = Field()          # 截止日期
    organizer = Field()         # 项目发起人
    item_id = Field()           # id
    address = Field()           # 地址
    des = Field()               # 简介
