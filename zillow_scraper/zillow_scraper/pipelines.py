# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request
from scrapy.exceptions import DropItem

from zillow_scraper import settings

import os
import re
import shutil


class ZillowScraperPipeline(object):
    def process_item(self, item, spider):
        # testing the pipeline
        if item['price']:
            item['price'] = item['price'][1:]
            return item

# manual image pipeline
class ZillowImagesPipeline(ImagesPipeline):
    # create request for every image url
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    # stuffs to do after the request is completed
    def item_completed(self, results, item, info):
        # iterate over all the local paths of downloaded images
        for result in [x for ok, x in results if ok]:
            # get default path
            path = result['path']
            
            # create arbitary path
            my_path = self.structurized(item)

            # default image store
            storage = settings.IMAGES_STORE

            # path to new directory
            target_path = os.path.join(storage, my_path)
            # image name
            filename = os.path.basename(path)
            # path to original image
            path = os.path.join(storage, path)

            if not os.path.exists(target_path):
                os.makedirs(target_path)
            shutil.move(path, target_path)
        return item
            
    def structurized(self, item):
        state = re.sub(r'[ :,]+', '_', item['state'])
        city = re.sub(r'[ :,]+', '_', item['city'])
        address = re.sub(r'[ :,]+', '_', item['address'])
        path = "/".join([state, city, address])
        return path




