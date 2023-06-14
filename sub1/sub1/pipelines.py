# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
import os
import pymysql

class Sub1Pipeline:
    def file_path(self, request, response=None, info=None):
        # 파일 경로 지정
        nttId = request.meta['nttId']
        file_sn = request.meta['file_sn']
        # 작업 경로에 'sub01' 폴더 생성
        base_dir = os.getcwd()
        sub01_dir = os.path.join(base_dir, 'sub01')
        os.makedirs(sub01_dir, exist_ok=True)

        # 파일명 설정
        file_name = f"{nttId}_{file_sn}.jpg"
        file_path = os.path.join(sub01_dir, file_name)

        return file_path

    def process_item(self, item, spider):
        # DB에 저장
        # self.save_to_database(item)

        return item

    def save_to_database(self, item):
        # # DB 연결 설정
        # db_host = 'localhost'
        # db_user = 'root'
        # db_password = '1234'
        # db_name = 'prac03'
        #
        # # DB 연결
        # connection = pymysql.connect(host=db_host, user=db_user, password=db_password, db=db_name)
        # cursor = connection.cursor()
        #
        # # 아이템 데이터 추출
        # nttId = item['nttId']
        # title = item['title']
        # wdate = item['wdate']
        # author = item['author']
        # readcount = item['readcount']
        # contentnum = item['contentnum']
        #
        # # DB에 데이터 삽입
        # query = "INSERT INTO your_table_name (nttId, title, wdate, author, readcount, contentnum) VALUES (%s, %s, %s, %s, %s, %s)"
        # values = (nttId, title, wdate, author, readcount, contentnum)
        # cursor.execute(query, values)
        # connection.commit()
        #
        # # DB 연결 종료
        # connection.close()
        pass
