# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import logging
import pymongo


class MongoPipeline(object):

    collection_name = "posts"
    """str: The name of the collection in the database (MongoDB)."""

    def __init__(self, mongo_uri, mongo_db):
        """Insert the crawled information to MongoDB.
        Args:
            mongo_uri: The MongoDB URI from the settings.py
            mongo_db: The MongoDB database name from the settings.py
        """
        self.__mongo_uri = mongo_uri
        self.__mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        """Pull in information from settings.py"""
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        """Initializing spider."""
        # Opening db connection.
        self.__client = pymongo.MongoClient(self.__mongo_uri)
        self.__db = self.__client[self.__mongo_db]

    def close_spider(self, spider):
        """Clean up when spider is closed."""
        self.__client.close()

    def process_item(self, item, spider):
        """Insert each post into the database collection."""
        self.__db[self.collection_name].insert(dict(item))
        logging.debug("Post added to MongoDB.")
        return item
