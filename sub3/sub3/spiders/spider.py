import scrapy
from .. import items

class NewsSpider(scrapy.Spider):
    name = "sub03"
    start_page = 1  # 크롤링 시작 페이지
    end_page = 2  # 크롤링 끝 페이지

    def start_requests(self):
        urls = [
            f"https://www.yna.co.kr/politics/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        # urls += [
        #     f"https://www.yna.co.kr/economy/all/{page}" for page in range(self.start_page, self.end_page + 1)
        # ]
        #
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 현재 페이지에서 기사 URL 추출
        article_links = response.xpath(
            '//*[@id="container"]/div/div/div[1]/section/div[1]/ul/li/div/div[2]/a/@href').getall()
        for article_link in article_links:
            yield response.follow(article_link, callback=self.parse_article)

    def parse_article(self, response):
        item = items.Sub3Item()

        item['title'] = response.css("header h1::text").get()
        item['author'] = response.css(".tit-name::text").get()
        date_xpath = "//span[@class='update-time']/text()"
        item['date'] = response.xpath("//p[@class='update-time']/text()[normalize-space()]").get()
        item['date'] = item['date'].strip() if item['date'] else None
        item['content'] = response.css(".story-news p::text").getall()
        yield item
