from scrapy.item import Item, Field
from scrapy.spiders import Spider, CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from bs4 import BeautifulSoup


class Article(Item):
    title = Field()
    description = Field()
    #link = Field()  


class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadoLibre'
    custom_settings = {
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36", 
        "CLOSESPIDER_PAGECOUNT": 20 ## Max number pages. 
    }

    ## Domains allowed to crawl
    allowed_domains = ['listado.mercadolibre.com.mx', 'articulo.mercadolibre.com.mx']

    start_urls = ['https://listado.mercadolibre.com.mx/celulares-smartphones/']

    ## Time between scraping each page
    download_delay = 1

    rules=(
        Rule(
            LinkExtractor(
                allow=r'/_Desde_\d+'), 
                follow=True), 
        Rule(
            LinkExtractor(
                allow=r'/MPE-'),
                follow=True, 
                callback='parse_items'),
    )


    ## Function to parse the items
    def parse_items(self, response):

        item = ItemLoader(Article(), response)
        ## get the title and description
        item.add_xpath('title', '//h1[@class="ui-pdp-title"]/text()')
        item.add_xpath('description', '//p[@class="ui-pdp-description__content"]/text()')


        yield item.load_item()  # return the item


# py -m scrapy runspider mercadolibre.py -o mercado_libre.json -t jsonlines

