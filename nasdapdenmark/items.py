# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CompanyItem(Item):
    industry = Field()
    fullname = Field()
    ccy = Field()
    last = Field()
    positiveornegative = Field()
    percent = Field()
    bid = Field()
    ask = Field()
    volume = Field()
    turnover = Field()
    pdflink = Field()