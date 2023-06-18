# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy import Item


class Sub3Item(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    sub_title = scrapy.Field()
    content = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()