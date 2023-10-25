# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
import hashlib
import datetime
import logging
import pytz
import os
import boto3
import logging

from .items import validate_item

class PropertyCrawlerPipeline:
    def process_item(self, item, spider):
        id = hashlib.sha1(item['url'].encode('utf-8')).hexdigest()
        item['id'] = id

        item['thumbnail'] = item['images'][0]

        item['initial_at'] = datetime.datetime.now(
            pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")
        
        item['update_at'] = datetime.datetime.now(
            pytz.timezone('Asia/Ho_Chi_Minh')).strftime("%Y-%m-%d %H:%M:%S")

        spider.logger.info(f'Item added: {item}')
        
        item = validate_item(item).dict()

        return item


class LoadToDynamodbPipeline:
    global urls_set 
    def open_spider(self, spider):
        urls_set = set()
        urls_set.add('HAHAHAHAHAHAHAHAH')
        self.session = boto3.Session(
            aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY'),
            region_name = os.environ.get('AWS_REGION'),
        )
 
        logging.info("Region name: %s", os.environ.get('AWS_REGION'))
        self.dynamodb_client = self.session.client('dynamodb')
        self.dynamodb_resource = self.session.resource('dynamodb')
        self.table = self.dynamodb_resource.Table(os.environ.get('DYNAMODB_RAW_TABLE'))

    def close_spider(self, spider):
        # self.session.close()
        pass

    def process_item(self, item, spider):
        # response = self.table.get_item(Key={'id': item['id], url: item['url']})
        self.table.put_item(Item = item)
        return item