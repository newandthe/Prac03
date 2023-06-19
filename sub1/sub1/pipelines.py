from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse, parse_qs
import os

import mysql.connector
from mysql.connector import Error

# MySQL 연결 설정
connection = mysql.connector.connect(
    host="localhost",
    database="prac03",  # 사용할 데이터베이스 스키마 이름
    user="root",  # MySql 사용자 이름
    password="1234"  # MySql 비밀번호 설정
)


# DB에 아이템을 삽입하는 함수
def insert_item_to_db(item):
    try:
        cursor = connection.cursor()

        # INSERT 쿼리
        query = "INSERT INTO sub01 (nttId, title, wdate, author, readcount, contentnum, image_urls, imgpath) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            item['nttId'],
            item['title'],
            item['wdate'],
            item['author'],
            item['readcount'],
            ' &&& '.join(item['contentnum']),
            ' &&& '.join(item['image_urls']),
            ' &&& '.join(item['imgpath'])
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()

    except Error as e:
        print("DB 삽입 에러 발생", e)


class CustomImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if 'image_urls' in item:
            images = item['image_urls']
            for image_url in images:
                yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)
        file_sn = query_params.get('fileSn', [''])[0]
        nttId = item['nttId']
        return f"{nttId}_{file_sn}.jpg"

    def item_completed(self, results, item, info):
        if 'image_urls' in item:
            item['imgpath'] = [x['path'] for ok, x in results if ok]

            # DB에 아이템 삽입
            insert_item_to_db(item)

        return item
