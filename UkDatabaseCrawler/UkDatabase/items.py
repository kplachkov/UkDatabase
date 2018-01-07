# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UkDatabaseItem(scrapy.Item):
    title = scrapy.Field()
    summary = scrapy.Field()
    text = scrapy.Field()
    post_pub_date = scrapy.Field()
    images = scrapy.Field()
