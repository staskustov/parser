# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from scrapy.loader.processors import MapCompose, TakeFirst
import scrapy

def cleaner_photo(value):
    if value[:2] == '//':
        return f'http:{value}'




class RealtyparserItem_avito(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    address = scrapy.Field(output_processor=TakeFirst())
    metro = scrapy.Field()
    price = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field()
    description = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    # phone = scrapy.Field()


class RealtyparserItem_cian(scrapy.Item):
    _id = scrapy.Field()
    address = scrapy.Field()
    metro = scrapy.Field()
    price = scrapy.Field()
    params = scrapy.Field()
    description = scrapy.Field()
    photos = scrapy.Field()
    #phone = scrapy.Field()
    link = scrapy.Field()