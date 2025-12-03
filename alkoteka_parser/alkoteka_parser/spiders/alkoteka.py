import scrapy
import json
import time
from datetime import datetime
from alkoteka_parser.items import ProductItem
from scrapy.utils.project import get_project_settings

class AlkotekaSpider(scrapy.Spider):
    name = "alkoteka"
    allowed_domains = ["alkoteka.com"]

    settings = get_project_settings()
    city_uuid = settings.get('CITY_UUID')
    start_urls = []

    # Формируем start_urls из категорий
    for url in settings.get('START_URLS', []):
        slug = url.rstrip('/').split('/')[-1]
        api_url = f"https://alkoteka.com/web-api/v1/product?city_uuid={city_uuid}&page=1&per_page=20&root_category_slug={slug}"
        start_urls.append(api_url)

    custom_settings = {
        'FEEDS': {
            'products.json': {'format': 'json', 'encoding': 'utf8'}
        }
    }

    def parse(self, response):
        data = json.loads(response.text)
        results = data.get('results', [])
        meta = data.get('meta', {})

        for product in results:
            product_slug = product.get('slug')
            if not product_slug:
                continue
            product_url = f"https://alkoteka.com/web-api/v1/product/{product_slug}?city_uuid={self.city_uuid}"
            yield scrapy.Request(product_url, callback=self.parse_product)

        current_page = meta.get('current_page', 1)
        has_more = meta.get('has_more_pages', False)
        if has_more:
            next_page = current_page + 1
            next_url = response.url.replace(f'page={current_page}', f'page={next_page}')
            yield scrapy.Request(next_url, callback=self.parse)

    def parse_product(self, response):
        data = json.loads(response.text)
        product = data.get('results', {})
        if not product:
            return

        item = ProductItem()
        item['timestamp'] = int(time.time())
        item['datetime'] = datetime.utcfromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        item['RPC'] = product.get('vendor_code')
        item['url'] = response.url
        item['title'] = product.get('name')
        item['brand'] = ''
        item['section'] = [
            product.get('category', {}).get('parent', {}).get('name', ''),
            product.get('category', {}).get('name', '')
        ]

        current_price = product.get('price') or 0
        prev_price = product.get('prev_price') or current_price
        sale_tag = ''
        if prev_price > current_price:
            discount = round((prev_price - current_price) / prev_price * 100)
            sale_tag = f"Скидка {discount}%"
        item['price_data'] = {
            'current': current_price,
            'original': prev_price,
            'sale_tag': sale_tag
        }

        total_quantity = product.get('quantity_total') or 0
        item['stock'] = {
            'in_stock': product.get('available', False),
            'count': total_quantity
        }

        main_image = product.get('image_url')
        item['assets'] = {
            'main_image': main_image,
            'set_images': [main_image] if main_image else [],
            'view360': [],
            'video': []
        }

        metadata = {}
        metadata['Артикул'] = product.get('vendor_code')
        for block in product.get('description_blocks', []):
            code = block.get('code')
            if code:
                if block.get('type') == 'select' and block.get('values'):
                    metadata[block.get('title')] = ', '.join([v.get('name') for v in block.get('values')])
                else:
                    metadata[block.get('title')] = f"{block.get('min', '')}-{block.get('max', '')} {block.get('unit', '')}".strip()

        text_blocks = product.get('text_blocks', [])
        if text_blocks:
            metadata['Описание'] = ' '.join([tb.get('content', '') for tb in text_blocks])
        item['metadata'] = metadata

        variants = []
        for block in product.get('description_blocks', []):
            if block.get('code') in ['obem', 'krepost']:
                variants.append({
                    'volume': block.get('min'),
                    'strength': next((b.get('min') for b in product.get('description_blocks', []) if b.get('code')=='krepost'), None)
                })
        item['variants'] = variants if variants else []

        item['marketing_tags'] = [label.get('title') for label in product.get('action_labels', [])]
        item['datetime'] = datetime.utcfromtimestamp(item['timestamp']).strftime('%Y-%m-%d %H:%M:%S')

        yield item
