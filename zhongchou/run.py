#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Author : Myx
# Time   : 2017/7/28 23:19
# File   : run.py

from scrapy import cmdline

if __name__ == '__main__':

    cmdline.execute('scrapy crawl zhongchouwang'.split())
    cmdline.execute('scrapy crawl Jd'.split())
    cmdline.execute('scrapy crawl kick'.split())
