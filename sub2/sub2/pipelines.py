import scrapy
from scrapy.pipelines.files import FilesPipeline
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
        query = "INSERT INTO sub02 (nttId, title_main, title_sub, wdate, author, readcount, content, filesrc, file_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (
            item['nttId'],
            ' &&& '.join(item['title_main']),
            item['title_sub'],
            item['wdate'],
            item['author'],
            item['readcount'],
            item['content'],
            ' &&& '.join(item['filesrc']),
            ' &&& '.join(item['file_path'])
        )
        cursor.execute(query, values)
        connection.commit()
        cursor.close()

    except Error as e:
        print("DB 삽입 에러 발생", e)


class CustomFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['filesrc']:
            yield scrapy.Request(file_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        file_name = item['filename'][item['filesrc'].index(request.url)]
        ntt_id = item['nttId']
        file_path = f"{ntt_id}_{file_name}"
        return file_path

    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if file_paths:
            item['file_path'] = file_paths

            # DB에 아이템 삽입
            insert_item_to_db(item)

        return item
