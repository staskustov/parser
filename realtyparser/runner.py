from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from realtyparser import settings_avito
from realtyparser import settings_cian
from realtyparser.spiders.avito import AvitoSpider
from realtyparser.spiders.cian import CianSpider

if __name__ == '__main__':
    crawler_settings_avito = Settings()
    crawler_settings_avito.setmodule(settings_avito)
    process_avito = CrawlerProcess(settings=crawler_settings_avito)

    crawler_settings_cian = Settings()
    crawler_settings_cian.setmodule(settings_cian)
    process_cian = CrawlerProcess(settings=crawler_settings_cian)


    process_avito.crawl(AvitoSpider)
    process_cian.crawl(CianSpider)
    process_avito.start()
    process_cian.start()