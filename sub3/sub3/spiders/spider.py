import scrapy


class QuotesSpider(scrapy.Spider):
    name = "sub03"

    firsturl = "https://www.yna.co.kr/"
    middleurl = "/all?site=navi_"
    # lasturl = "_depth02"

    def start_requests(self):
        firsturl = "https://www.yna.co.kr/"


    def parse_start(self, response):
        article_url = ""
