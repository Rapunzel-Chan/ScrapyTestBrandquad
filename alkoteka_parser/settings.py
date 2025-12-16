import os

from dotenv import load_dotenv

load_dotenv()

BOT_NAME = "alkoteka_parser"

SPIDER_MODULES = ["alkoteka_parser.spiders"]
NEWSPIDER_MODULE = "alkoteka_parser.spiders"

USER_AGENT = os.getenv(
    "USER_AGENT",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
)
ROBOTSTXT_OBEY = False  # выключен на время тестового

CITY_NAME = os.getenv("CITY_NAME", "Краснодар")
CITY_UUID = os.getenv("CITY_UUID", "4a70f9e0-46ae-11e7-83ff-00155d026416")

DOWNLOADER_MIDDLEWARES = {
    "alkoteka_parser.middlewares.RegionMiddleware": 543,
    "alkoteka_parser.middlewares.ProxyMiddleware": 544,
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,
}

FEED_EXPORT_ENCODING = "utf-8"
LOG_LEVEL = "INFO"
PROXIES = os.getenv("PROXIES", "").split(",")

CONCURRENT_REQUESTS = 4
DOWNLOAD_DELAY = 1.5
DOWNLOAD_TIMEOUT = 40

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 2
AUTOTHROTTLE_MAX_DELAY = 10

RETRY_TIMES = 5
RETRY_HTTP_CODES = [500, 502, 503, 504, 408, 429]
