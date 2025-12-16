import scrapy


class ProductItem(scrapy.Item):
    timestamp = scrapy.Field()
    RPC = scrapy.Field()  # уникальный код товара
    url = scrapy.Field()
    title = scrapy.Field()
    marketing_tags = scrapy.Field()  # список
    brand = scrapy.Field()
    section = scrapy.Field()  # иерархия категорий
    price_data = scrapy.Field()  # dict: current, original, sale_tag
    stock = scrapy.Field()  # dict: in_stock, count
    assets = scrapy.Field()  # dict: main_image, set_images, view360, video
    metadata = scrapy.Field()  # dict: характеристики
    variants = scrapy.Field()  # int
    datetime = scrapy.Field()
