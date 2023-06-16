import scrapy
from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse, parse_qs
import os

class CustomFilePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        for file_url in item['filesrc']:
            yield scrapy.Request(file_url, meta={'item': item})

    def file_path(self, request, response=None, info=None, *, item=None):
        item = request.meta['item']
        parsed_url = urlparse(request.url)
        query_params = parse_qs(parsed_url.query)
        file_id = query_params.get('atchFileId', [''])[0]
        file_name = item['filename'][item['filesrc'].index(request.url)]
        file_ext = os.path.splitext(file_name)[1]
        ntt_id = item['nttId']
        return f'{ntt_id}_{file_name}{file_ext}'


    def item_completed(self, results, item, info):
        file_paths = [x['path'] for ok, x in results if ok]
        if file_paths:
            item['file_path'] = file_paths
        return item
