# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from realtyparser.items import RealtyparserItem_cian
from scrapy.loader import ItemLoader
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC

class CianSpider(scrapy.Spider):
    name = 'cian'
    allowed_domains = ['cian.ru']
    start_urls = ['https://www.cian.ru/snyat-kvartiru-bez-posrednikov/']


    def parse(self, response):
        paginator = response.xpath("//div/ul//li[contains(@class, 'list-item')]/a/@href")
        for page in paginator:
            yield response.follow(page, callback=self.parse).extract()

        links = response.xpath("//div[contains(@class, 'card')]//a[contains(@class, 'header')]/@href").extract()
        for link in links:
            yield response.follow(link, callback=self.ads_parse)


    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=RealtyparserItem_cian(), response=response)
        loader.add_xpath('address', '//address/a/text()')
        loader.add_xpath('metro', '//ul/li/a[contains(@class, "underground_link")]/text()')
        loader.add_xpath('price', '//span[@itemprop="price"]/text()')
        loader.add_xpath('params', '//div[contains(@class, "info-value")]/text()')
        loader.add_xpath('description', '//p[@itemprop="description"]/text()')
        loader.add_value('link', response.url)



        driver = webdriver.Chrome(executable_path='/Users/staskustov/PycharmProjects/realty_parser/venv/chromedriver')
        driver.get(response.url)
        action = ActionChains(driver)
        loader.add_xpath('phone', '//div[contains(@class, "print_phones")]/text')
        thumbs = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class, "fotorama__nav__frame fotorama__nav__frame--thumb")]')))
        action.move_to_element(thumbs[-1]).click().perform()

        photos = [i.find_element_by_xpath(".//img").get_attribute('src') for i in thumbs]
        driver.quit()

        loader.add_value('photos', photos)

        yield loader.load_item()