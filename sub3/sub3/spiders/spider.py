import scrapy
from .. import items
import re


class QuotesSpider(scrapy.Spider):
    name = "sub03"
    start_page = 1  # 크롤링 시작 페이지
    end_page = 2  # 크롤링 끝 페이지

    def start_requests(self):
        urls = [
            f"https://www.yna.co.kr/politics/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/economy/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/north-korea/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/industry/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/society/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/local/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/international/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/culture/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/lifestyle/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/entertainment/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/sports/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/opinion/advisory/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/opinion/editorials/{page}" for page in range(self.start_page, self.end_page + 1)
        ]
        urls += [
            f"https://www.yna.co.kr/people/all/{page}" for page in range(self.start_page, self.end_page + 1)
        ]


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
