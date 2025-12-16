import json
import time
from datetime import datetime

import scrapy
from scrapy.utils.project import get_project_settings

from alkoteka_parser.items import ProductItem
from alkoteka_parser.start_urls import START_URLS
from alkoteka_parser.utils.categories import extract_slug


class AlkotekaSpider(scrapy.Spider):
    """
    Запускает паука через прокси из .env, если он не срабатывает, запускает парсер
    """

    name = "alkoteka"
    allowed_domains = ["alkoteka.com"]

    custom_settings = {
        "FEEDS": {
            "products.json": {
                "format": "json",
                "encoding": "utf8",
            }
        }
    }

    def start_requests(self):
        settings = get_project_settings()
        self.city_uuid = settings.get("CITY_UUID")

        for category_url in START_URLS:
            category_slug = extract_slug(category_url)
            if not category_slug:
                continue

            api_url = (
                "https://alkoteka.com/web-api/v1/product"
                f"?city_uuid={self.city_uuid}"
                "&page=1"
                "&per_page=20"
                f"&root_category_slug={category_slug}"
            )

            yield scrapy.Request(
                api_url,
                callback=self.parse,
                meta={"category_slug": category_slug},
            )

    def parse(self, response):
        try:
            data = json.loads(response.text)
        except Exception:
            self.logger.warning(f"Не удалось получить данные по URL: {response.url}, пропускаем")
            return

        results = data.get("results", [])
        meta = data.get("meta", {})
        category_slug = response.meta.get("category_slug")

        for product in results:
            product_slug = product.get("slug")
            if not product_slug:
                continue

            product_url = f"https://alkoteka.com/web-api/v1/product/" f"{product_slug}?city_uuid={self.city_uuid}"

            yield scrapy.Request(
                product_url,
                callback=self.parse_product,
                meta={
                    "product_slug": product_slug,
                    "category_slug": category_slug,
                },
            )

        current_page = meta.get("current_page", 1)
        has_more = meta.get("has_more_pages", False)

        if has_more:
            next_page = current_page + 1
            next_url = response.url.replace(
                f"page={current_page}",
                f"page={next_page}",
            )
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                meta=response.meta,
            )

    def parse_product(self, response):
        product_slug = response.meta.get("product_slug")
        category_slug = response.meta.get("category_slug")

        try:
            data = json.loads(response.text)
        except Exception:
            self.logger.warning(f"Не удалось получить данные по товару: {response.url}")
            return

        product = data.get("results")
        if not product:
            return

        item = ProductItem()

        timestamp = int(time.time())
        item["timestamp"] = timestamp
        item["datetime"] = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        item["RPC"] = product.get("vendor_code")
        item["url"] = f"https://alkoteka.com/product/" f"{category_slug}/{product_slug}"
        item["title"] = product.get("name")
        item["brand"] = ""
        item["section"] = [
            product.get("category", {}).get("parent", {}).get("name", ""),
            product.get("category", {}).get("name", ""),
        ]

        current_price = product.get("price") or 0
        prev_price = product.get("prev_price") or current_price

        sale_tag = ""
        if prev_price > current_price:
            discount = round((prev_price - current_price) / prev_price * 100)
            sale_tag = f"Скидка {discount}%"

        item["price_data"] = {
            "current": current_price,
            "original": prev_price,
            "sale_tag": sale_tag,
        }

        item["stock"] = {
            "in_stock": product.get("available", False),
            "count": product.get("quantity_total") or 0,
        }

        main_image = product.get("image_url")
        item["assets"] = {
            "main_image": main_image,
            "set_images": [main_image] if main_image else [],
            "view360": [],
            "video": [],
        }

        metadata = {"Артикул": product.get("vendor_code")}

        for block in product.get("description_blocks", []):
            title = block.get("title")
            if not title:
                continue

            if block.get("type") == "select" and block.get("values"):
                metadata[title] = ", ".join(v.get("name", "") for v in block.get("values", []))
            else:
                value = f"{block.get('min', '')}-{block.get('max', '')} {block.get('unit', '')}".strip()
                if value:
                    metadata[title] = value

        text_blocks = product.get("text_blocks", [])
        if text_blocks:
            metadata["Описание"] = " ".join(tb.get("content", "") for tb in text_blocks)

        item["metadata"] = metadata

        item["variants"] = 0
        item["marketing_tags"] = [label.get("title") for label in product.get("action_labels", [])]

        yield item
