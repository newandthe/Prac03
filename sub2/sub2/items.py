# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


from datetime import datetime
from scrapy import Field
from scrapy import Item
now = datetime.now()

class Sub2Item(scrapy.Item):
    nttId2 = scrapy.Field
    title_main = scrapy.Field() # 메인 제목
    title_sub = scrapy.Field() # 서브 제목
    wdate = scrapy.Field() # 등록일
    author = scrapy.Field() # 작성자
    readcount = scrapy.Field() # 조회수
    content = scrapy.Field() # 글 내용
    
    # 아래는 파일
    filepath = Field() # 파일 저장경로
    filename = scrapy.Field() # 파일 이름
