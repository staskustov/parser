# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.python import to_bytes
import hashlib
import os


class Data_cleaner:
    def process_item(self, item, spider):
        if spider.name == 'avito':
            item['address'] = item['address'].replace('\n', '')[1: -1]
            item['name'] = item['name'].replace('\n', '')[1: -1]
            item['price'] = int(item['price'].replace(' ', ''))

            item['params'][1] = int(item['params'][1].replace(' ', ''))
            item['params'][3] = int(item['params'][3].replace(' ', ''))
            item['params'][5] = item['params'][5].replace(' ', '')

            if item['params'][7] == 'студии ':
                item['params'][7] = 'студия'
            else:
                item['params'][7] = int(item['params'][7].split('-')[0])

            item['params'][9] = float(item['params'][9].replace('\xa0', '').replace(' ', '').replace('м²', ''))

            item['params'] = {'floor': item['params'][1], 'house_floors': item['params'][3], 'house_type': item['params'][5],
                              'rooms': item['params'][7], 'apart_area': item['params'][9]}

        if spider.name == 'cian':
            item['address'] = item['address']
            item['metro'] = item['metro']
            item['price'] = item['price']
            item['params'] = item['params']
            item['description'] = item['description']


        return item




class PhotoPiplene(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item['photos']:
            for image in item['photos']:
                try:
                    yield scrapy.Request(image, meta={'item': item})
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]

        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        name = item['address']
        url = request.url
        media_guid = hashlib.sha1(to_bytes(url)).hexdigest()
        media_ext = os.path.splitext(url)[1]
        return f'full/{name}/%s%s' % (media_guid, media_ext)





class Realtyparser_insert_MDB:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.realty_ads

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        collection.insert_one(item)
        return item



