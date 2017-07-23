#!/usr/bin/env python3
# -*- coding:utf-8 -*- 
# Author : Myx
# Time   : 2017/7/14 18:18
# File   : analyse.py

import pygal
from pymongo import MongoClient
import time
from flask import Flask,Response

db = MongoClient('localhost', 27017).panda
collection = db.panda
posts = db.posts

l = []
for p in list(posts.find()):
    l.append(p['room_number'])
num100W=[]
num10W = []
num1W=[]
num5000=[]
num1000=[]
num500=[]
num100=[]
num50=[]
num00=[]
for x in l:
    if int(x) >= 1000000:
        num100W.append(x)
    elif 100000 <= int(x) < 1000000:
        num10W.append(x)
    elif 10000 <= int(x) < 100000:
        num1W.append(x)
    elif 5000 <= int(x) < 10000:
        num5000.append(x)
    elif 1000 <= int(x) < 50000:
        num1000.append(x)
    elif 500 <= int(x) < 1000:
        num500.append(x)
    elif 100 <= int(x) < 500:
        num100.append(x)
    elif 50 <= int(x) < 100:
        num50.append(x)
    elif 0 <= int(x) < 50:
        num00.append(x)

app = Flask(__name__)
@app.route('/')
def index():
    return """
        <html>
        <body>
            <h1>hello pygal and flask</h1>
            <figure>
            <embed type="image/svg+xml" src="/hellosvg/" />
            <embed type="image/svg+xml" src="/hellosvg1/" />
            </figure>
        </body>
        </html>'
            """
@app.route('/hellosvg/')
def graph():
    pie = pygal.Pie()
    pie.title = '7.14 20:30 不同人气主播分布比(%)'
    pie.add('>100W', 100 * len(num100W) / posts.count())
    pie.add('10W~100W', 100 * len(num10W) / posts.count())
    pie.add('1W~10W', 100 * len(num1W) / posts.count())
    pie.add('5K~1W', 100 * len(num5000) / posts.count())
    pie.add('1K~5K', 100 * len(num1000) / posts.count())
    pie.add('500~1K', 100 * len(num500) / posts.count())
    pie.add('100~500', 100 * len(num100) / posts.count())
    pie.add('50~100', 100 * len(num50) / posts.count())
    pie.add('<50', 100 * len(num00) / posts.count())
    # return Response(
    #     response=pie.render_to_file('不同人气主播分布比%s.svg' % time.time()),
    #     content_type='image/svg+xml')
    # pie.render_to_file('不同人气主播分布比%s.svg' % time.time())
    return Response(
        response=pie.render(),
        content_type='image/svg+xml',
    )

@app.route('/hellosvg1/')
def graph1():
    pie1 = pygal.Pie(print_values=True, value_formatter=lambda x: '{:.3f}'.format(x))
    pie1.title = '7.14 20:30 主播所占人气比(%)'
    pie1.add('>100W',  100 * sum(map(int, num100W)) / sum(map(int, l)),formatter=lambda x: '%.3f' % x)
    pie1.add('10W~100W', 100 * sum(map(int, num10W)) / sum(map(int, l)))
    pie1.add('1W~10W', 100 * sum(map(int, num1W)) / sum(map(int, l)))
    pie1.add('5K~1W', 100 * sum(map(int, num5000)) / sum(map(int, l)))
    pie1.add('1K~5K', 100 * sum(map(int, num1000)) / sum(map(int, l)))
    pie1.add('500~1K', 100 * sum(map(int, num500)) / sum(map(int, l)))
    pie1.add('100~500', 100 * sum(map(int, num100)) / sum(map(int, l)))
    pie1.add('50~100', 100 * sum(map(int, num50)) / sum(map(int, l)))
    pie1.add('<50', 100 * sum(map(int, num00)) / sum(map(int, l)))
    # return Response(
    #     response=pie1.render_to_file('不同人气主播分布比%s.svg' % time.time()),
    #     content_type='image/svg+xml')
    # pie1.render_to_file('主播所占人气比%s.svg' % time.time())
    return Response(
        response=pie1.render(),
        content_type='image/svg+xml',
    )

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5880, debug=True)




