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
    nttId = scrapy.Field()
    domain = Field()
    title_main = scrapy.Field()  # 메인 제목
    title_sub = scrapy.Field()  # 서브 제목
    wdate = scrapy.Field()  # 등록일
    author = scrapy.Field()  # 작성자
    readcount = scrapy.Field()  # 조회수
    content = scrapy.Field()  # 글 내용
    url_link = Field()
    category = Field()
    filesrc = scrapy.Field() # 파일 다운로드 링크
    filename = scrapy.Field() # 파일 명 어떻게 저장할지 ..

    #  FilesPipeline에서는 [ 'files', 'file_urls' ] 두개의 Field를 갖는 Item을 반환해야 한다.
    # 아래는 파일
    file_urls = Field()
    files = Field()
    file_path = scrapy.Field()
