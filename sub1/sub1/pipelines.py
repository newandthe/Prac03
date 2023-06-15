from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from urllib.parse import urlparse, parse_qs
import os

import pymysql


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
        return item