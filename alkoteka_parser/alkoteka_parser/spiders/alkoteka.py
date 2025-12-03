import scrapy
import json
import time
import re
from datetime import datetime
from alkoteka_parser.items import ProductItem


class AlkotekaProductsSpider(scrapy.Spider):
    name = 'alkoteka'
    allowed_domains = ['alkoteka.com']

    # Список ссылок на категории
    start_urls = [
        'https://alkoteka.com/web-api/v1/product?city_uuid=4a70f9e0-46ae-11e7-83ff-00155d026416&page=1&per_page=20&root_category_slug=slaboalkogolnye-napitki-2'
    ]

    custom_settings = {
        'FEEDS': {
            'products.json': {'format': 'json', 'encoding': 'utf8'}
        },
        'DOWNLOADER_MIDDLEWARES': {
            'alkoteka_parser.middlewares.RegionMiddleware': 543,
        }
    }

    def parse(self, response):
        data = json.loads(response.text)
        results = data.get('results', [])

        for product in results:
            product_url = response.urljoin(product.get('product_url'))
            yield scrapy.Request(product_url, callback=self.parse_product)

        # Пагинация
        meta = data.get('meta', {})
        current_page = meta.get('current_page', 1)
        has_more = meta.get('has_more_pages', False)
        if has_more:
            next_page = current_page + 1
            next_url = response.url.replace(f'page={current_page}', f'page={next_page}')
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_product(self, response):
        item = ProductItem()
        item['timestamp'] = int(time.time())

        # RPC (артикул)
        rpc = response.css('.product-card__header p::text').re_first(r'\d+')
        item['RPC'] = rpc if rpc else ''

        item['url'] = response.url

        # Название товара
        title = response.css('h1::text').get()
        volume = response.css('.product-card__tags button p::text').re_first(r'\d+\.?\d*\s*[лL]')
        if volume:
            title = f"{title}, {volume}"
        item['title'] = title

        # Marketing tags
        item['marketing_tags'] = response.css('.product-card__tags button p::text').getall()

        # Brand
        item['brand'] = response.css('.specifications-card:contains("Бренд") p::text').get(default='').strip()

        # Section (категории)
        item['section'] = response.css('.breadcrumbs__item span::text').getall()

        # Price data
        current_price_text = response.css('.cart-card__sale-price .text--body-bold::text').re_first(r'\d+')
        original_price_text = response.css('.cart-card__sale-price .text--tag::text').re_first(r'\d+')
        current_price = float(current_price_text) if current_price_text else 0
        original_price = float(original_price_text) if original_price_text else current_price
        sale_tag = ''
        if original_price > current_price:
            discount = round((original_price - current_price) / original_price * 100)
            sale_tag = f"Скидка {discount}%"
        item['price_data'] = {
            'current': current_price,
            'original': original_price,
            'sale_tag': sale_tag
        }

        # Stock
        in_stock_text = response.css('.product-card__interactives-anchor a::text').re_first(r'\d+')
        in_stock = int(in_stock_text) > 0 if in_stock_text else False
        item['stock'] = {
            'in_stock': in_stock,
            'count': int(in_stock_text) if in_stock_text else 0
        }

        # Assets
        main_image = response.css('.product-info__hero-img-wrap img::attr(src)').get()
        set_images = response.css('.product-info__hero-img-wrap img::attr(src)').getall()
        item['assets'] = {
            'main_image': main_image,
            'set_images': set_images,
            'view360': [],
            'video': []
        }

        # Metadata
        metadata = {}
        metadata['__description'] = response.css('.product-info__description-text::text').get(default='').strip()
        for spec in response.css('.specifications-card'):
            key = spec.css('span::text').get()
            value = spec.css('p::text').get()
            if key and value:
                metadata[key.strip()] = value.strip()
        metadata['Артикул'] = rpc
        item['metadata'] = metadata

        # Variants
        item['variants'] = len(response.css('.product-card__tags button p::text').re(r'\d+\.?\d*\s*[лL]'))

        yield item
