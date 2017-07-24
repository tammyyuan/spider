# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import json

class HrqqPipeline(object):

    def __init__(self):
        self.filename = open("tencent.json",'w')

    def process_item(self,item, spider):
        text = json.dumps(dict(item),ensure_ascii=False) + ',\n'
        try:
            self.filename.write(text)
        except Exception as error:
            print("写入失败",text)
            print(type(text.encode('utf-8')))
            print(error)
        return item

    def close_spide(self):
        self.filename.close()

    # def process_item(self, item, spider):
    #     return item
