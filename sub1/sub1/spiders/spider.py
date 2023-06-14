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
        # item['nttId'] = response.xpath(링크로 구하기!!!)
        # 데이터 가공하기 !!!
        item['title'] = response.xpath('//*[@id="print_area"]/form/div[1]/h4/text()').get()
        item['wdate'] = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[1]/text()').get()
        item['author'] = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[2]/text()').get()
        item['readcount'] = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[3]/text()').get()

        item['imgnum'] = response.xpath('//*[@id="print_area"]/form/div[1]/div[3]/div/ul/li/p/a/@href').getall()
        item['contentnum'] = response.xpath('//*[@id="print_area"]/form/div[1]/div[3]/div/ul/li/p/text()').getall()

        item['imgpath'] = response.xpath('//*[@id="print_area"]/form/div[1]/dl[1]/dd/div/ul/li/a[1]/@href').getall() # 링크에 모두 https://www.mois.go.kr/ 앞에 붙여주기
        yield item
