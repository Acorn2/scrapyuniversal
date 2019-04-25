# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import NewsItem
from scrapyuniversal.loaders import *
from scrapy.loader.processors import TakeFirst, Identity
from scrapy.utils.spider import iterate_spider_output
from scrapy.http import Request, HtmlResponse
import copy
import six


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(
            LinkExtractor(allow=r'article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
            callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="pages"]/a[contains(text(),"下一页")]'))
        # 当callback为空的时候，follow默认为True，follow为True是时，代表继续跟进匹配分析
    )


    def _build_request(self, rule, link, base_url):
        r = Request(url=link.url, callback=self._response_downloaded, meta={'base_url': base_url})
        r.meta.update(rule=rule, link_text=link.text)
        return r

    def _requests_to_follow(self, response):
        # 重写该方法，只是稍作修改
        base_url = response.url
        # print('base_url------------{}'.format(base_url))
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                     if lnk not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            for link in links:
                seen.add(link)
                r = self._build_request(n, link, base_url)
                yield rule.process_request(r)


    def parse_item(self, response):
        base_url = response.meta['base_url']
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_value('base_page_url', base_url)
        loader.add_xpath('news_title', '//h1[@id="chan_newsTitle"]/text()')
        loader.add_value('news_url', response.url)
        loader.add_xpath('news_text', '//div[@id="chan_newsDetail"]//text()')
        loader.add_xpath('news_publish_time', '//div[@id="chan_newsInfo"]/text()', re='(\d+-\d+-\d+\s\d+:\d+:\d+)')
        loader.add_xpath('news_source', '//div[@id="chan_newsInfo"]/text()', re='来源：(.*)')
        loader.add_value('news_website', '中华网')

        yield loader.load_item()

    # def parse_item(self, response):
    #     item = NewsItem()
    #     #新闻标题
    #     item['news_title'] = response.xpath('//h1[@id="chan_newsTitle"]/text()').extract_first()
    #     #新闻详情地址
    #     item['news_url'] = response.url
    #     #新闻内容
    #     item['news_text'] = ''.join(response.xpath('//div[@id="chan_newsDetail"]//text()').extract()).strip().replace('\n','').replace('\t','').replace('\r','')
    #     #新闻发布时间
    #     # item['news_publish_time'] = response.xpath('//div[@class="chan_newsInfo_link"]/text()').re_first('(\d+-\d+-\d+\s\d+:\d+:\d+)')
    #     item['news_publish_time'] = response.xpath('//div[@id="chan_newsInfo"]/text()').re_first('(\d+-\d+-\d+\s\d+:\d+:\d+)')
    #     #新闻来源
    #     item['news_source'] = response.xpath('//div[@id="chan_newsInfo"]/text()').re_first('来源(.*)')
    #     item['news_website'] = '中华网'
    #
    #     yield item