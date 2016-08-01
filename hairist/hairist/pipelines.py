# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

from hairist import settings

import os
import shutil


class HairistPipeline(object):
    def process_item(self, item, spider):
        return item

class HairistImagePipeline(ImagesPipeline):
    # create request for every image url
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    # stuffs to do after the request is completed
    def item_completed(self, results, item, info):
        for result in [x for ok, x in results if ok]:
            print("="*30)
            # original path
            path = result['path']

            # get full storage path
            storage = settings.IMAGES_STORE

            # new folder name according to id
            my_path = str(result['id'])


            # new path according to id
            new_path = os.path.join(storage, my_path)

            # filename
            filename = os.path.basename(path)

            # path to original image
            path = os.path.join(storage, path)

            # new path
            target_path = os.path.join(storage, my_path)

            # now move to the new path
            if not os.path.exists(target_path):
                os.makedirs(target_path)
            shutil.move(path, target_path)
        return item




