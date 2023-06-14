import scrapy
from scrapy import Spider

from .. import items


class QuotesSpider(scrapy.Spider):
    # 스파이더 이름(실행 시)
    name = "sub01"

    def start_requests(self):
        url = 'https://www.mois.go.kr/frt/bbs/type002/commonSelectBoardList.do?bbsId=BBSMSTR_000000000010'
        yield scrapy.Request(url, self.parse_start)

    # 게시물 상세 페이지 url로 request
    def parse_start(self, response):
        article_url = "https://www.mois.go.kr"
        article_id = response.xpath('//*[@id="print_area"]/div[2]/form/ul/li/a/@href').getall()
        for d in article_id:
            url = article_url + d
            yield scrapy.Request(url, self.parse_article)

    # 게시물에서 정보 크롤링
    def parse_article(self, response):
        item = items.Sub1Item()
        item['title'] = response.xpath('//*[@id="print_area"]/form/div[1]/h4/text()').get()
        yield item
