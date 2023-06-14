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
        article_url = "https://www.mois.go.kr/frt/bbs/type002/commonSelectBoardArticle.do?bbsId=BBSMSTR_000000000010"
        data_no = response.xpath('//*[@id="print_area"]/div[2]/form/ul/li[1]/a').getall()

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

    # 상게 게시물에서 정보 크롤링 시작.