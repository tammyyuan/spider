# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.downloadermiddlewares.defaultheaders import DefaultHeadersMiddleware
from scrapy.http.headers import Headers
import threading
import requests
from zhongchou import settings
import random


class ZhongchouDefaultHeadersMiddleware(DefaultHeadersMiddleware):

    def process_request(self, request, spider):
        user_agent = random.choice(settings.AGENTS)

        if spider.name == 'zhongchouwang':
            referer = 'http://www.zhongchou.com/'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': referer,
                'User-Agent': user_agent,
            }
        elif spider.name == 'Jd':
            referer = 'https://z.jd.com/bigger/search.html'
            path = request.url.split('com')[-1]
            headers = {
                ':authority': 'z.jd.com',
                ':method': 'GET',
                ':path': path,
                ':scheme': 'https',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
                'accept-Encoding': 'gzip, deflate, br',
                'cache-control': 'max-age=0',
                'referer': referer,
                'upgrade-insecure-requests': '1',
                'user-agent': user_agent,
            }
        # elif spider.name == 'taobao':
        #     referer = 'https://izhongchou.taobao.com/index.htm'
        else:
            referer = 'https://www.kickstarter.com/'
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.6,en;q=0.4',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Host': 'www.kickstarter.com',
                'Referer': referer,
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': user_agent,
            }

        h = Headers(seq=headers)
        request.headers = h

class ZhongchouUserAgentMiddleware(UserAgentMiddleware):
    def process_request(self, request, spider):
        agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        request.headers['User-Agent'] = agent

class ZhongchouProxyMiddleware(object):
    proxy_pool = []
    def process_request(self, request, spider):
        proxy = self.get_proxy()
        print('request ip: %s' % proxy)
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):
        if response.status != 200:
            proxy = self.get_proxy()
            print('response  ip: %s' % proxy)
            request.meta['proxy'] = proxy
            return request
        return response

    def get_proxy(self):
        t = threading.Thread(target=self.validateProxy)
        t.start()
        # proxy = self.validateProxy()
        if self.proxy_pool:
            proxy = self.proxy_pool[0]
            self.proxy_pool.pop(0)
        else:
            proxy = ''
        return proxy


    def validateProxy(self):
        while len(self.proxy_pool) < 10:
            while True:
                r = requests.get('http://127.0.0.1:5000/get/').text
                pro = 'http://' + r
                proxy = {'http': pro}
                try:
                    r = requests.get('https://www.baidu.com/', proxies=proxy, timeout=2)
                    if r.status_code == 200:
                        self.proxy_pool.append(pro)
                        break
                    else:
                        print('删除代理 !200', proxy)
                        requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(r))
                except BaseException as e:
                    print('删除代理', proxy)
                    requests.get("http://127.0.0.1:5000/delete/?proxy={}".format(r))


class ZhongchouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
