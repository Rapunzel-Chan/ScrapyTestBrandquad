import scrapy
import json

class AlkotekaLinksSpider(scrapy.Spider):
    """
    Выгружает в products.json наименования и url продуктов
    """
    name = 'alkoteka_links'
    allowed_domains = ['alkoteka.com']

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
            yield {
                'name': product.get('name'),
                'product_url': product.get('product_url')
            }

        meta = data.get('meta', {})
        current_page = meta.get('current_page', 1)
        has_more = meta.get('has_more_pages', False)

        if has_more:
            next_page = current_page + 1
            next_url = response.url.replace(f'page={current_page}', f'page={next_page}')
            yield scrapy.Request(next_url, callback=self.parse, cookies=response.request.cookies)
