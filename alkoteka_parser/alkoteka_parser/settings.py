BOT_NAME = 'alkoteka_parser'

SPIDER_MODULES = ['alkoteka_parser.spiders']
NEWSPIDER_MODULE = 'alkoteka_parser.spiders'

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.5
DOWNLOAD_TIMEOUT = 40

DOWNLOADER_MIDDLEWARES = {
    'alkoteka_parser.middlewares.RegionMiddleware': 543,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
}

FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'INFO'
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10
RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
