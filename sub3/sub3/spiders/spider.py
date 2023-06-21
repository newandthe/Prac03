import scrapy
from .. import items
import re


class QuotesSpider(scrapy.Spider):
    name = "sub03"
    start_page = 1  # 크롤링 시작 페이지

    def start_requests(self):
        urls = [
            f"https://www.yna.co.kr/politics/all/{self.start_page}",
            f"https://www.yna.co.kr/economy/all/{self.start_page}",
            f"https://www.yna.co.kr/north-korea/all/{self.start_page}",
            f"https://www.yna.co.kr/industry/all/{self.start_page}",
            f"https://www.yna.co.kr/society/all/{self.start_page}",
            f"https://www.yna.co.kr/local/all/{self.start_page}",
            f"https://www.yna.co.kr/international/all/{self.start_page}",
            f"https://www.yna.co.kr/culture/all/{self.start_page}",
            f"https://www.yna.co.kr/lifestyle/all/{self.start_page}",
            f"https://www.yna.co.kr/entertainment/all/{self.start_page}",
            f"https://www.yna.co.kr/sports/all/{self.start_page}",
            f"https://www.yna.co.kr/opinion/advisory/{self.start_page}",
            f"https://www.yna.co.kr/opinion/editorials/{self.start_page}",
            f"https://www.yna.co.kr/people/all/{self.start_page}"
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        article_links = response.xpath(
            '//*[@id="container"]/div/div/div[1]/section/div[1]/ul/li/div/div[2]/a/@href').getall()
        for article_link in article_links:
            yield response.follow(article_link, callback=self.parse_article)

        # 현재 페이지의 숫자를 추출
        current_page = int(response.css('div.paging.paging-type01 strong.num.on::text').get())

        # 다음 페이지의 숫자를 계산
        next_page = current_page + 1

        # 다음 페이지의 URL을 생성
        next_page_url = response.url.replace(f"/{current_page}", f"/{next_page}")

        # 다음 페이지로 이동하기 전에 다음 페이지의 링크 유무를 확인
        next_page_link = response.css('div.paging.paging-type01 a.num::attr(href)').get()
        if not next_page_link:
            next_page_link = response.css('div.paging.paging-type01 a.next::attr(href)').get()
            if not next_page_link:
                return

        # 다음 페이지로 이동
        yield response.follow(next_page_url, callback=self.parse)

    def parse_article(self, response):
        item = items.Sub3Item()

        url = response.url
        item['url_link'] = url

        pattern = r'AKR(\d{17})'
        match = re.search(pattern, url)

        if match:
            nttid = match.group(0)
            item['nttId'] = nttid

        category = response.xpath('//*[@id="articleWrap"]/div[1]/header/ul[1]/li[2]/a/text()').get()
        item['category'] = category or "북한"

        item['main_title'] = response.css("header h1::text").get()
        item['sub_title'] = response.xpath('//*[@id="articleWrap"]/div[2]/div/div/article/div[2]/h2/text()').getall()
        item['author'] = response.css(".tit-name::text").getall()
        date_xpath = "//span[@class='update-time']/text()"
        item['date'] = response.xpath("//p[@class='update-time']/text()[normalize-space()]").get()
        item['date'] = item['date'].strip() if item['date'] else None
        content = response.css(".story-news p::text").getall()
        content = [c.strip() for c in content if c.strip()]
        item['content'] = ' '.join(content)
        imgsrc = response.xpath('//*[@id="articleWrap"]/div[2]/div/div/article/div/figure/div/span/img/@src').getall()
        item['imgsrc'] = ['https:' + url for url in imgsrc]

        yield item
