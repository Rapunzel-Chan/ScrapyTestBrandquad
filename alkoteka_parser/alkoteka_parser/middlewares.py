# middlewares.py
from scrapy import signals
from urllib.parse import quote
import time

class RegionMiddleware:
    """Устанавливает нужные куки для региона и подтверждения возраста"""

    def process_request(self, request, spider):
        request.cookies['alkoteka_locality'] = '{"uuid":"4a70f9e0-46ae-11e7-83ff-00155d026416","name":"Краснодар"}'
        request.cookies['alkoteka_geo'] = 'true'
        request.cookies['alkoteka_age_confirm'] = 'true'
        request.cookies['alkoteka_cookies'] = 'true'
        time.sleep(0.3)

