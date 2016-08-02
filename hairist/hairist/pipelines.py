# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
from scrapy.http import Request

from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

from hairist import settings
from hairist.models import Hairist, db_connect, DeclarativeBase

import os
import shutil
import glob


class HairistPipeline(object):
    def process_item(self, item, spider):
        return item

class PostgresPipeline:

    def __init__(self):
        self.collection_name = "hairist"

    def open_spider(self, spider):
        self.createdb()

    def process_item(self, item, spider):
        if item:
            self.insert(item)
        return item

    def createdb(self):
        engine = db_connect()
        DeclarativeBase.metadata.create_all(engine)

    def insert(self, item):
        try:
            engine = db_connect()
            Session = sessionmaker(bind=engine)
            session = Session()

            mapper = inspect(Hairist)
            attr_names = [c_attr.key for c_attr in mapper.mapper.column_attrs]

            d = {}
            for attr in attr_names:
                try:
                    d[attr] = str(item[attr])
                    #print(type(d[attr]), attr,  d[attr])
                except KeyError:
                    d[attr] = ''
            amp = Hairist(**d)
            session.add(amp)
            session.commit()
            session.close()
        except IntegrityError:
            print("="*50)
            print("already exists... cannot insert")
            return


class HairistImagePipeline(ImagesPipeline):
    # create request for every image url
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    # stuffs to do after the request is completed
    def item_completed(self, results, item, info):
        path = None
        for result in [x for ok, x in results if ok]:
            try:
                print("="*30)
                # original path
                path = result['path']

                # get full storage path
                storage = settings.IMAGES_STORE

                # new folder name according to id
                my_path = str(item['id'])


                # new path according to id
                new_path = os.path.join(storage, my_path)

                # filename
                filename = os.path.basename(path)

                # path to original image
                path = os.path.join(storage, path)

                # new path
                target_path = os.path.join(storage, my_path)

                item['image_local_path'] = target_path

                # now move to the new path
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                shutil.move(path, target_path)
            except shutil.Error:
                os.remove(path)
                continue
        return item




