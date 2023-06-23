from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse, parse_qs
import os

import pymysql
import hashlib

conn = pymysql.connect(host='172.30.1.100',
                       port=3306,
                       db="prac01",  # 사용할 데이터베이스 스키마 이름
                       user="jsk",  # MySql 사용자 이름
                       password="1234",
                       charset='utf8')


# DB에 아이템을 삽입하는 함수
def insert_item_to_db(item):
    try:
        cursor = conn.cursor()

        # INSERT 쿼리 (테이블)
        sql = "INSERT INTO sub04 (nttId, domain, title, wdate, author, readcount, content, url_link, category) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(sql, (
            item['nttId'],
            item['domain'],
            item['title'],
            item['wdate'],
            item['author'],
            item['readcount'],
            ' &&& '.join(item['contentnum']),
            item['url_link'],
            item['category']
            # ' &&& '.join(item['image_urls']),
            # ' &&& '.join(item['imgpath'])
        )
        )

        # INSERT 쿼리 (데이터)
        sql = "INSERT INTO datafile (nttId, origin_name, file_hash, filesrc) VALUES (%s, %s, %s, %s)"

        nttId = item['nttId']
        original_filename = item['original_filename']
        imgpath = item['imgpath']
        imgsrc = item['imgsrc']

        listlen = len(original_filename)

        for i in range(listlen):
            cursor.execute(sql, (
                nttId,
                original_filename[i],
                imgpath[i],
                imgsrc[i]
            ))

        conn.commit()
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

        # 파일 경로에 폴더 경로와 파일 이름을 추가하여 반환
        return f"{nttId}/{nttId}_{file_sn}.jpg"

    def item_completed(self, results, item, info):
        if 'image_urls' in item:
            # 이미지 다운로드 경로 대신 파일 이름으로 item['imgpath']에 저장
            item['imgpath'] = [x['path'] for ok, x in results if ok]

            # DB에 아이템 삽입
            insert_item_to_db(item)

        return item

