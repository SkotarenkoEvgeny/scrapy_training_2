# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import json
from tauntondeeds.items import TauntondeedsItem

class TauntondeedsPipeline(object):

    def open_spider(self, spider):
        self.file = open('output.json', 'w', encoding="utf8")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):

        for field in item.fields:
            item.setdefault(field, None)
        line = json.dumps(dict(item), default=str) + "\n"
        self.file.write(line)

        return item

