import pymongo
from bson.json_util import dumps
from pymongo import MongoClient

from UkDatabaseAPI.database.database import Database
from UkDatabaseAPI.database.query_builder.mongo_query_builder import MongoQueryBuilder

MONGO_URI = "mongodb://localhost:27017"
"""str: The MongoDB URI."""


class MongoDB(Database):

    def __init__(self):
        """Client for a MongoDB instance."""
        # Opening db connection.
        self.__client = MongoClient(MONGO_URI)
        self.__db = self.__client.UkDatabase

    def __del__(self):
        """Close the connection."""
        self.close_connection()

    def crate_collection_text_index(self):
        """Create a text index for the collection."""
        self.__db.posts.create_index([('TEXT', pymongo.TEXT)], name='text', default_language='english')

    def close_connection(self):
        """Close the connection."""
        self.__client.close()

    def find_posts(self, text: str, post_pub_date: str, number_of_results: int) -> str:
        """Find posts containing text or/and within a time range.
        Args:
            text: The text search criterion, from the URL argument.
            post_pub_date: The date or time range search criterion, from the URL argument.
            number_of_results: The number of results to return, from the URL argument.
        Returns:
            The posts containing the text or/and within a time range.
        """
        queries = {}
        if text:
            queries.update(MongoQueryBuilder
                           .get_query_for_search_by_text(text))
        if post_pub_date:
            queries.update(MongoQueryBuilder
                           .get_query_for_search_by_post_date(post_pub_date))
        result = self.__db.posts.find({"$and": [queries]}, {"score": {"$meta": "textScore"}})
        if number_of_results:
            # If int argument provided by the URL, the results are limited and sorted.
            result = result.sort([("score", {"$meta": "textScore"})]).limit(number_of_results)
        else:
            # Return all matched results sorted.
            result = result.sort([("score", {"$meta": "textScore"})])
        return dumps(result)
