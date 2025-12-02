# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AlkotekaParserItem(scrapy.Item):
    """Класс с полями данных."""
    timestamp = scrapy.Field()  # int
    RPC = scrapy.Field()  # str
    url = scrapy.Field()  # str
    title = scrapy.Field()  # str
    marketing_tags = scrapy.Field()  # list
    brand = scrapy.Field()  # str
    section = scrapy.Field()  # list
    price_data = scrapy.Field()  # dict
    stock = scrapy.Field()  # dict
    assets = scrapy.Field()  # dict
    metadata = scrapy.Field()  # dict
    variants = scrapy.Field()  # int
