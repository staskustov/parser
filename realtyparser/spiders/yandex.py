# -*- coding: utf-8 -*-
import scrapy


class YandexSpider(scrapy.Spider):
    name = 'yandex'
    allowed_domains = ['realty.yandex.ru']
    start_urls = ['http://realty.yandex.ru/']

    def parse(self, response):
        pass
