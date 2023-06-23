import hashlib

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter
import mysql.connector
from mysql.connector import Error

import pymysql

conn = pymysql.connect(host='172.30.1.100',
                       port=3306,
                       db="prac01",  # 사용할 데이터베이스 스키마 이름
                       user="jsk",  # MySql 사용자 이름
                       password="1234",
                       charset='utf8')
# cursor = conn.cursor()
#
# sql = ''

# MySQL 연결 설정
# connection = mysql.connector.connect(
#     host="localhost",
#     database="prac03",  # 사용할 데이터베이스 스키마 이름
#     user="root",  # MySql 사용자 이름
#     password="1234"  # MySql 비밀번호 설정
# )


# DB에 아이템을 삽입하는 함수
def insert_item_to_db(item):
    try:
        cursor = conn.cursor()

        # INSERT 쿼리
        sql = "INSERT INTO sub04 (nttId, category, domain, title, sub_title, wdate, author, content, url_link) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, (item['nttId'],
                       item['category'],
                       item['domain'],
                       item['main_title'],
                       ' &&& '.join(item['sub_title']),
                       item['date'],
                       ' &&& '.join(item['author']),
                       item['content'],
                       item['url_link'],
                       # ' &&& '.join(item['imgsrc'])
                       ))

        # INSERT 쿼리 (데이터)
        sql = "INSERT INTO datafile (nttId, file_hash, filesrc) VALUES (%s, %s, %s)"
        nttId = item['nttId']
        # 이미지를 그냥 긁어오는 형태라 원본 파일 이름은 존재하지 않는다.
        file_hash = item['file_path']
        imgsrc = item['imgsrc']

        listlen = len(imgsrc)

        for i in range(listlen):
            cursor.execute(sql, (
                nttId,
                file_hash[i],
                imgsrc[i]
            ))


        conn.commit()
        cursor.close()
    except Error as e:
        print("DB 삽입 에러 발생", e)


class Sub3Pipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        if 'imgsrc' in item:
            images = item['imgsrc']
            for image_url in images:
                yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, *, info=None):
        item = request.meta['item']
        nttid = item['nttId']
        sha256_hash = hashlib.sha256(request.url.encode()).hexdigest()
        image_guid = f"{nttid}/{sha256_hash}.jpg"
        if 'file_path' not in item:
            item['file_path'] = []
        item['file_path'].append(sha256_hash)  # SHA-256 해시값을 리스트에 추가
        return image_guid

    def item_completed(self, results, item, info):
        if 'imgsrc' in item:
            img_urls = [x['url'] for ok, x in results if ok]
            item['file_path'] = [item['nttId'] + "/" + hashlib.sha256(url.encode()).hexdigest() + ".jpg" for url in img_urls]

            # DB에 아이템 삽입
            insert_item_to_db(item)

        return item


