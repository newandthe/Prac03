import scrapy
from scrapy import Spider
from .. import items

from urllib.parse import urljoin

import re
import hashlib

class QuotesSpider(scrapy.Spider):
    # 스파이더 이름(실행 시)
    name = "sub01"

    custom_settings = {
        'ITEM_PIPELINES': {'sub1.pipelines.CustomImagesPipeline': 1}
    }

    def start_requests(self):
        url = 'https://www.mois.go.kr/frt/bbs/type002/commonSelectBoardList.do?bbsId=BBSMSTR_000000000010&searchCnd=&searchWrd=&pageIndex=%s'  # %s
        start_page = 1  # start page 정의
        for i in range(433):  # 1부터 3번 페이지까지 (i는 0부터 시작)
            yield scrapy.Request(url % (i + start_page), self.parse_start)

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

        item['category'] = "행안부 이미지"
        item['domain'] = "mois"
        item['nttId'] = nttId
        item['title'] = response.xpath('//*[@id="print_area"]/form/div[1]/h4/text()').get()
        wdate_text = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[1]/text()').get()
        if wdate_text:
            wdate = wdate_text.replace('등록일 : ', '').strip()
            wdate = wdate.replace('.', '')
            wdate = wdate[:4] + '-' + wdate[4:6] + '-' + wdate[6:]

        else:
            wdate = None

        item['wdate'] = wdate

        author_text = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[2]/text()').get()
        if author_text:
            item['author'] = author_text.replace('작성자 : ', '')
        else:
            item['author'] = None

        readcount_text = response.xpath('//*[@id="print_area"]/form/div[1]/div[2]/span[3]/text()').get()
        if readcount_text:
            readcount = int(readcount_text.replace('조회수 : ', ''))
        else:
            readcount = 0

        item['readcount'] = readcount

        # rel_img_urls = response.xpath('//*[@id="print_area"]/form/div[1]/div[3]/div/ul/li/p/a/@href').getall()

        imgsrc_list = response.xpath('//*[@id="print_area"]/form/div[1]/div[3]/div/ul/li/p/a/@href').getall()

        item['imgsrc'] = [urljoin('https://www.mois.go.kr/', path) for path in imgsrc_list]

        content_list = response.xpath('//*[@id="print_area"]/form/div[1]/div[3]/div/ul/li/p/text()').getall()
        item['contentnum'] = [content.strip() for content in content_list if content.strip()]

        imgpath_list = response.xpath('//*[@id="print_area"]/form/div[1]/dl[1]/dd/div/ul/li/a[1]/@href').getall()
        item['imgpath'] = [urljoin('https://www.mois.go.kr/', path) for path in imgpath_list]

        # 더러운 파일이름 파싱
        original_filenames = response.xpath('//*[@id="print_area"]/form/div[1]/dl[1]/dd/div/ul/li/a[1]/text()').getall()
        cleaned_filenames = []

        for filename in original_filenames:
            split_filename = filename.split()
            if split_filename:
                cleaned_filename = split_filename[0].strip()
                cleaned_filenames.append(cleaned_filename)
        item['original_filename'] = cleaned_filenames

        item['image_urls'] = self.url_join(imgpath_list, response)
        # print(item)
        yield item

    def url_join(self, rel_img_urls, response):
        joined_urls = []
        for rel_img_url in rel_img_urls:
            joined_urls.append(response.urljoin(rel_img_url))

        return joined_urls






