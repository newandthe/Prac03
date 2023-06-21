import scrapy
from scrapy.pipelines.files import FilesPipeline
import os
import mysql.connector
from mysql.connector import Error

import pymysql


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

        # INSERT 쿼리
        sql = "INSERT INTO sub02 (nttId, title_main, title_sub, wdate, author, readcount, content, filesrc, file_path) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute (sql, (
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
        )
        conn.commit()
        cursor.close()

    except Error as e:
        print("DB 삽입 에러 발생", e)


class Sub2Pipeline(FilesPipeline):
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
