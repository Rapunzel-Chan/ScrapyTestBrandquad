from scrapy import signals
from urllib.parse import quote
import time

import os
import random
from dotenv import load_dotenv

load_dotenv()

class RegionMiddleware:
    """Устанавливает нужные куки для региона и подтверждения возраста."""
    def process_request(self, request, spider):
        request.cookies['alkoteka_locality'] = '{"uuid":"4a70f9e0-46ae-11e7-83ff-00155d026416","name":"Краснодар"}'
        request.cookies['alkoteka_geo'] = 'true'
        request.cookies['alkoteka_age_confirm'] = 'true'
        request.cookies['alkoteka_cookies'] = 'true'


class ProxyMiddleware:
    """Использует прокси из .env; если список пустой, работает без прокси."""
    def __init__(self):
        proxies_env = os.getenv("PROXIES", "")
        self.proxies = [p.strip() for p in proxies_env.split(",") if p.strip()]

    def process_request(self, request, spider):
        if self.proxies:
            request.meta['proxy'] = random.choice(self.proxies)
