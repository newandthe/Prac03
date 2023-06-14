# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from datetime import datetime

now = datetime.now()

class Sub1Item(scrapy.Item):
    # nttId = scrapy.Field() # 게시물 번호 (URL 에서 parsing 해야 하지 않을까 싶음.. 필수!!  보류)
    title = scrapy.Field() # 글 제목
    wdate = scrapy.Field() # 등록일
    author = scrapy.Field() # 작성자
    readcount = scrapy.Field() # 조회수
    # cdate = now.strftime('$Y-%m-%d %H:%M:%S')   # ex) 2021-12-22 15:46:26
    imgnum = scrapy.Field() # 각각의 이미지들이 몇번째에 해당하는 이미지인지 구하기 위한 용도.
    contentnum = scrapy.Field() # 몇번째 이미지에 해당하는 본문들인지 알기 위한 용도.

    imgpath = scrapy.Field() # 이미지를 다운로드 받기 위한 URL ( URL에 입력시 바로 다운로드 됨 )

