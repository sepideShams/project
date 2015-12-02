# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Field
from scrapy_djangoitem import DjangoItem

class EqItem(scrapy.Item):
    Origin_Time = scrapy.Field()
    Magnitude = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    Depth = scrapy.Field()
    Region = scrapy.Field()
