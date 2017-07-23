# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):

    job_name = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    workYear = scrapy.Field()
    education = scrapy.Field()
    publish_time = scrapy.Field()
    advantage = scrapy.Field()  # 职位诱惑
    description = scrapy.Field()  # 职位描述
    job_area = scrapy.Field()  # 工作地
    company_name = scrapy.Field()
    company_fullname = scrapy.Field()
    industryField = scrapy.Field()  # 行业
    financeStage = scrapy.Field()  # 融资情况
    companySize = scrapy.Field()
    job_id = scrapy.Field()
    kd = scrapy.Field()

    '''
    def item2dict(self):
        return {
            'kd': self.kd,
            'job_name': self.job_name,
            'salary': self.salary,
            'city': self.city,
            'workYear': self.workYear,
            'education': self.education,
            'publish_time': self.publish_time,
            'company_name': self.company_name,
            'job_area': self.job_area,
            'company_fullname': self.company_fullname,
            'industryField': self.industryField,
            'financeStage': self.financeStage,
            'companySize': self.companySize,
            'job_id': self.job_id,
            'advantage': self.advantage,
            'description': self.description,
        }
    '''


