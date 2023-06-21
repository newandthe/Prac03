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
        sql = "INSERT INTO sub03 (nttId, category, author, wdate, title, content, imgpath, url_link, sub_title) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.execute(sql, (item['nttId'],
                       item['category'],
                       ' &&& '.join(item['author']),
                       item['date'],
                       item['main_title'],
                       item['content'],
                       ' &&& '.join(item['imgsrc']),
                       item['url_link'],
                       ' &&& '.join(item['sub_title'])))

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
        image_guid = request.url.split('/')[-1]
        return f"{nttid}_{image_guid}"

    def item_completed(self, results, item, info):
        if 'imgsrc' in item:
            img_urls = [x['url'] for ok, x in results if ok]
            item['imgsrc'] = img_urls

            # DB에 아이템 삽입
            insert_item_to_db(item)

        return item
