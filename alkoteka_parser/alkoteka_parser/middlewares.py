# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AlkotekaParserRegionMiddleware:
    """Класс для парсинга по указанному региону"""
    def __init__(self, region_id):
        self.region_id = region_id

    @classmethod
    def from_crawler(cls, crawler):
        region_id = crawler.settings.get('REGION_ID', '736')  # ID Краснодар
        return cls(region_id)

    def process_request(self, request, spider):
        request.cookies['region_id'] = self.region_id
        return None


class AlkotekaParserProxyMiddleware:
    """Класс со списком прокси"""
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get('PROXY_LIST', [])
        return cls(proxy_list)

    def process_request(self, request, spider):
        if self.proxy_list:
            proxy = random.choice(self.proxy_list)
            request.meta['proxy'] = proxy
            spider.logger.debug(f"Using proxy: {proxy}")
        return None
