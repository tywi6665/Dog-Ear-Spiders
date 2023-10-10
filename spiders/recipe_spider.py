import scrapy
from dog_ear_spiders.items import DogEarSpidersItem
import re


class RecipeSpider(scrapy.Spider):
    name = 'recipe_spider'

    # Dynamic methods that allows Django to pass values to crawler
    def __init__(self, *args, **kwargs):
        # going to pass these args from django view 
        # To make everything dynamic, we need to override them inside __init__ method
        self.url = kwargs.get('url')
        self.domain = kwargs.get('domain')
        self.start_urls = [self.url]
        self.allowed_domains = [self.domain]

    def parse(self, response):
        self.logger.info('--------Now scaping------- %s', self.url)
        self.logger.info('--------Domain------- %s', self.domain)

        # Defining defaults
        url = response.url
        title = ''
        img_src = ''
        author = ''
        description = ''

        try:
            title = response.xpath("//meta[@property='og:title']/@content")[0].extract()
        except:
            print('An error has occurred while scraping the title')
        try:
           img_src= response.xpath("//meta[@property='og:image']/@content")[0].extract()
        except:
            print('An error has occurred while scraping the image src')
        try:
           author = response.xpath("//meta[@name='sailthru.author']/@content")[0].extract()
        except:
            print('An error has occurred while scraping the author')
        try:
           description = response.xpath("//meta[@property='og:description']/@content")[0].extract()
        except:
            print('An error has occurred while scraping the description')

        self.logger.info('--------Item------- %s', {
            'url': response.url,
            'title': title,
            'img_src': img_src,
            'author': author,
            'description': description,
        })

        yield {
            'url': response.url,
            'title': title,
            'img_src': img_src,
            'author': author,
            'description': description,
        }
        