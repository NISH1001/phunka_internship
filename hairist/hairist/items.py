# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HairistItem(scrapy.Item):
    id                      = scrapy.Field() # id
    yetkili                 = scrapy.Field() # authorized
    kuafor_salonu_turu      = scrapy.Field() # barber shop type
    calisma_saatleri        = scrapy.Field() # working hours
    tatil_gunleri           = scrapy.Field() # vacation days
    koltuk_sayisi           = scrapy.Field() # no. of seats
    kullanilan_markalar     = scrapy.Field() # used brands
    telfon                  = scrapy.Field() # telephone
    mobil                   = scrapy.Field() # mobile
    adres                   = scrapy.Field() # address
    ilce_il                 = scrapy.Field() # town_city
    email                   = scrapy.Field() # email
    latlng                  = scrapy.Field() # google map coordinate
    image_urls              = scrapy.Field()
    images                  = scrapy.Field()
    image_local_path        = scrapy.Field()
