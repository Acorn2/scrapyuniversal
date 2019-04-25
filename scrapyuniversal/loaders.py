#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/21 10:34
software: PyCharm
description: 
'''
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Join, Compose,Identity


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()


class ChinaLoader(NewsLoader):
    news_text_out = Compose(Join(), lambda s: s.strip().replace('\n','').replace('\t','').replace('\r\n',''))
    news_source_out = Compose(Join(), lambda s: s.strip().replace('\n','').replace('\t','').replace('\r\n',''))
