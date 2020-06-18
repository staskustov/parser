# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from realtyparser.items import RealtyparserItem_avito
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC



class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    def __init__(self):
        self.start_urls = ['https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?cd=1&user=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//span[@data-marker="pagination-button/next"]').extract_first()
        links = response.xpath('//h3/a[@class="snippet-link"]/@href').extract()
        for link in links:
            yield response.follow(link, callback=self.ads_parse)
        yield response.follow(next_page, callback=self.parse)


    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=RealtyparserItem_avito(), response=response)
        loader.add_xpath('address', '//div/span[@class="item-address__string"]/text()')
        loader.add_xpath('metro', '//span[@class="item-address-georeferences-item__content"]/text()')
        loader.add_xpath('price', '//span[@class="js-item-price"]/text()')
        loader.add_xpath('params', '//li[@class="item-params-list-item"]/text()')
        loader.add_xpath('description', '//div[@class="item-description-text"]/p/text()')
        loader.add_xpath('photos', '//div[@class="gallery-img-frame js-gallery-img-frame"]/@data-url')
        loader.add_xpath('name', '//div[@class="seller-info-name js-seller-info-name"]/a/text()')
        loader.add_value('link', response.url)
        # loader.add_xpath('phone', )

        # driver = webdriver.Chrome(executable_path='/Users/staskustov/PycharmProjects/realty_parser/venv/chromedriver')
        # driver.get(response.url)
        # button = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(By.XPATH, '//div[@class="item-phone-number js-item-phone-number greenContact_color"]'))
        # button.click()



        yield loader.load_item()



