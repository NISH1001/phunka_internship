# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

from zillow_scraper import settings

import os


class ZillowScraperPipeline(object):
    def process_item(self, item, spider):
        # testing the pipeline
        if item['price']:
            item['price'] = item['price'][1:]
            return item

class ZillowImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_complete(self, results, item, info):
        pass
