# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZillowScraperItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    zip_code = scrapy.Field()
    beds = scrapy.Field()
    baths = scrapy.Field()
    sq_ft = scrapy.Field()
    price = scrapy.Field()
    facts = scrapy.Field()
    features = scrapy.Field()
    appliances_included = scrapy.Field()
    room_types = scrapy.Field()
    construction = scrapy.Field()
    other = scrapy.Field()
    county_website = scrapy.Field()
    #agents = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
