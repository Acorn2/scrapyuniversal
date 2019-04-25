# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyuniversalItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class NewsItem(scrapy.Item):

    base_page_url = scrapy.Field()#当前列表页url
    news_title = scrapy.Field()#新闻标题
    news_url = scrapy.Field()#新闻详情地址
    news_text = scrapy.Field()#新闻内容
    news_publish_time = scrapy.Field()#新闻发布时间
    news_source = scrapy.Field()#新闻来源
    news_website = scrapy.Field()#新闻站点

