import scrapy
from scrapy import Spider

from .. import items


class QuotesSpider(scrapy.Spider):
    # 스파이더 이름(실행)
    name = "sub02"

    custom_settings = {
        'ITEM_PIPELINES': {'sub1.pipelines.CustomImagesPipeline': 1}
    }

    def start_request(self):
        url = "https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&searchCnd=&searchWrd=&pageIndex=%s"
        start_page = 1  # start page 정의
        for i in range(1):  # 1부터 1번 페이지까지 (i는 0부터 시작)
            yield scrapy.Request(url % (i + start_page), self.parse_start)

    # 게시물 상세 페이지 url로 request
    def parse_start(self, response):
        article_url = "https://www.mois.go.kr"
        article_id = response.xpath('//*[@id="print_area"]/div[2]/form/table/tbody/tr[4]/td/div/a/@href').getall()
        for d in article_id:
            url = article_url + d
            yield scrapy.Request(url, self.parse_article)

    # 게시물에서 정보 크롤링
    def parse_article(self, response):
        item = items.Sub2Item()

