# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import scrapy
from scrapy.pipelines.images import ImagesPipeline
from itemadapter import ItemAdapter


class Sub3Pipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item.get('image_urls', []):
            yield scrapy.Request(image_url, meta={'item': item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        ntt_id = item['ntt_id']
        image_guid = request.url.split('/')[-1]
        filename = f'nttId_{ntt_id}_{image_guid}'
        return filename

    def item_completed(self, results, item, info):
        adapter = ItemAdapter(item)
        images = [x for ok, x in results if ok]
        adapter['images'] = images
        return item
