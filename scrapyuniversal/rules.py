#!/usr/bin/env python
# -*- coding:utf-8 -*-
'''
author:Herish
datetime:2019/4/21 20:22
software: PyCharm
description: 爬取规则属性
'''
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule

rules = {
    'china': (
        Rule(
            LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),callback='parse_item'),
        # Rule(LinkExtractor(restrict_xpaths='//div[@class="pageStyle"]//a[contains(.,"下一页")]'))#当callback为空的时候，follow默认为True，follow为True是时，代表继续跟进匹配分析
    )
}
