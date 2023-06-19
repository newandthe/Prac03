# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
from scrapy import Item


class Sub3Item(scrapy.Item):

    nttId = scrapy.Field()
    category = scrapy.Field()
    main_title = scrapy.Field()
    sub_title = scrapy.Field()
    author = scrapy.Field()
    date = scrapy.Field()
    sub_title = scrapy.Field()
    content = scrapy.Field()
    url_link = scrapy.Field()
    imgsrc = scrapy.Field()

    # 크롤링 이미지 다운로드에 필요한 필수 요소 두가지
    image_urls = scrapy.Field()
    images = scrapy.Field()

    imgpath = scrapy.Field() # 파일이 저장될 제목