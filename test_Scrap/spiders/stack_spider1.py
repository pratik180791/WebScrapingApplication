# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import HtmlXPathSelector

from scrapy import Spider
from scrapy.selector import Selector
from test_Scrap.items import TestScrapItem
from test_Scrap.items import AmazonItem
import datetime



class StackSpider1Spider(CrawlSpider):

    name = 'stack_spider1'
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest"
    ]



    def parse(self, response):
        now = datetime.datetime.now()
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = TestScrapItem()
            item['title'] = question.xpath(
                'a[@class="question-hyperlink"]/text()').extract()[0]
            item['url'] = 'https://stackoverflow.com'+question.xpath(
                'a[@class="question-hyperlink"]/@href').extract()[0]
            item['date']=now
            yield item
