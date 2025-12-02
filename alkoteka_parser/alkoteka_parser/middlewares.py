# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
from scrapy.exceptions import NotConfigured
from twisted.internet.error import TimeoutError, DNSLookupError, ConnectionRefusedError
from scrapy import signals
import random

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AlkotekaParserRegionMiddleware:
    """Класс для парсинга по указанному региону."""
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
    """Класс со списком прокси."""
    def __init__(self, proxy_list):
        if not proxy_list:
            raise NotConfigured("PROXY_LIST is empty")
        self.proxy_list = proxy_list
        self.dead_proxies = set()

    @classmethod
    def from_crawler(cls, crawler):
        proxy_list = crawler.settings.get('PROXY_LIST')
        if not proxy_list:
            raise NotConfigured("PROXY_LIST is not set")
        return cls(proxy_list)

    def process_request(self, request, spider):
        working_proxies = [p for p in self.proxy_list if p not in self.dead_proxies]

        if not working_proxies:
            spider.logger.warning("No working proxies available")
            return None

        proxy = random.choice(working_proxies)
        request.meta['proxy'] = proxy
        request.meta['download_timeout'] = 15
        spider.logger.debug(f"Using proxy: {proxy}")
        return None

    def process_exception(self, request, exception, spider):
        proxy = request.meta.get('proxy')

        if proxy and isinstance(exception, (TimeoutError, DNSLookupError, ConnectionRefusedError)):
            self.dead_proxies.add(proxy)
            spider.logger.warning(f"Proxy failed: {proxy} - {exception}")

            working_proxies = [p for p in self.proxy_list if p not in self.dead_proxies]
            if working_proxies:
                new_proxy = random.choice(working_proxies)
                new_request = request.copy()
                new_request.meta['proxy'] = new_proxy
                new_request.dont_filter = True
                spider.logger.info(f"Retrying with new proxy: {new_proxy}")
                return new_request

        return None
