# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ResultItem(scrapy.Item):
    usn = scrapy.Field()
    name = scrapy.Field()
    sem = scrapy.Field()
    branch = scrapy.Field()
    sgpa = scrapy.Field()
    subjects = scrapy.Field(serializer=list)
