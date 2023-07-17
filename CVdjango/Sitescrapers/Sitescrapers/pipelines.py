# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo

from CVdjango.Sitescrapers.Sitescrapers.items import SiteItem
from CVdjango.Sitescrapers.Sitescrapers.spiders.researchgate import Researchgate


class SitescrapersPipeline:

    collection_name = "Candinates"

    def __init__(self, mongo_uri, mongo_db):
        try:
            self.mongo_uri = mongo_uri
            self.mongo_db = mongo_db
        except Exception as error:
            print(error)
            print("Problem")
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
        )

    def open_spider(self, spider):
        try:
            self.client = pymongo.MongoClient(self.mongo_uri)
            self.db = self.client[self.mongo_db]
            print(self.db)
            print('KAPPA')
        except Exception as error:
            print(error)
            print("Problem to Inizilize tje DB")
    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, Researchgate):
            try:
                self.db[self.collection_name].update_one(
                    {'name': spider.author},  # Query part
                    {'$push': {'Researchgate.papers': dict(item)}},  # Update part
                    upsert=True  # This will create a new document if the candidate does not exist
                )
            except Exception as error:
                print(error)
                print("We have problem with insert/update")
        elif isinstance(item, SiteItem):
            try:
                self.db[self.collection_name].update_one(
                    {'name': spider.author},  # Query part
                    {'$set': {'Researchgate.url': item['researchgate_url']}},  # Update part
                    upsert=True  # This will create a new document if the candidate does not exist
                )
            except Exception as error:
                print(error)
                print("We have problem with insert/update")
        return item
