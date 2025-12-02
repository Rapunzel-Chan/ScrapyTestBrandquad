# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class AlkotekaParserPipeline:
    """Класс для возврата данных полей"""
    def process_item(self, item, spider):
        return item


class JsonWriterPipeline:
    """Класс для запуска паука и записи в файл result.json."""
    def open_spider(self, spider):
        self.file = open('result.json', 'w', encoding='utf-8')
        self.file.write('[')

    def close_spider(self, spider):
        self.file.write(']')
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        self.file.write(line)
        return item
