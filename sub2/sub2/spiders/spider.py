import scrapy
from scrapy import Spider
from .. import items
import mysql.connector
from mysql.connector import Error

from urllib.parse import urljoin

import re

import hashlib


class QuotesSpider(scrapy.Spider):
    # 스파이더 이름(실행)
    name = "sub02"

    custom_settings = {
        'ITEM_PIPELINES': {'sub2.pipelines.Sub2Pipeline': 1}
    }

    def start_requests(self):
        url = "https://www.mois.go.kr/frt/bbs/type010/commonSelectBoardList.do?bbsId=BBSMSTR_000000000008&searchCnd=&searchWrd=&pageIndex=%s"
        start_page = 1  # start page 정의
        for i in range(1452):  # 1부터 3번 페이지까지 (i는 0부터 시작)
            yield scrapy.Request(url % (i + start_page), self.parse_start)

    # 게시물 상세 페이지 url로 request
    def parse_start(self, response):
        article_url = "https://www.mois.go.kr"
        article_id = response.xpath('//*[@id="print_area"]/div[2]/form/table/tbody/tr/td[2]/div/a/@href').extract()
        for d in article_id:
            url = article_url + d
            yield scrapy.Request(url, self.parse_article)

    # 게시물에서 정보 크롤링
    def parse_article(self, response):
        item = items.Sub2Item()

        # 게시물의 URL에서 nttId 추출
        # 게시물의 URL에서 nttId 추출
        url = response.url
        item['url_link'] = url
        url_bytes = url.encode('utf-8')

        # SHA-256 해시 객체 생성
        sha256_hash = hashlib.sha256()

        # URL의 해시값 계산
        sha256_hash.update(url_bytes)

        # 해시값 추출
        hash_value = sha256_hash.hexdigest()

        nttId = hash_value

        item['category'] = "행안부 파일"
        item['domain'] = "mois"
        item['nttId'] = nttId

        title_main = response.xpath('//*[@id="print_area"]/form/div/h4/text()').extract()
        item['title_main'] = [t.strip() for t in title_main if t.strip()]

        title_sub = response.xpath('//*[@id="print_area"]/form/div/h4/span/text()').extract()
        title_sub = [ts.strip() for ts in title_sub if ts.strip()]
        item['title_sub'] = ' '.join(title_sub)

        text = response.xpath('/html/body/div/div[8]/div/div[2]/div[4]/form/div/div[2]/text()').extract()
        wdate_parsed = text[2].split(':')[-1].strip()
        wdate = wdate_parsed.replace('.', '')
        wdate = wdate[:4] + '-' + wdate[4:6] + '-' + wdate[6:]
        item['wdate'] = wdate
        item['author'] = text[4].split(':')[-1].strip()
        item['readcount'] = text[6].split(':')[-1].strip()

        content = response.xpath('//*[@id="desc_mo"]/text()').getall()
        content = [c.strip() for c in content if c.strip()]
        item['content'] = ' '.join(content)

        filesrc = response.xpath(
            '//*[@id="print_area"]/form/div/dl[1]/dd/div/ul/li/a[1]/@href').getall()  # + https://mois.go.kr 추가 # 다운로드 링크
        item['filesrc'] = ['https://mois.go.kr/' + url for url in filesrc]

        filename = response.xpath('//*[@id="print_area"]/form/div/dl[1]/dd/div/ul/li/a[1]/text()').getall()
        parsed_filenames = []
        for fn in filename:
            parsed_fn = re.search(r'(\d{6}.*\.(hwpx|pdf|hwp))', fn)
            if parsed_fn:
                parsed_filenames.append(parsed_fn.group(1))

        item['filename'] = parsed_filenames

        yield item
