# -*- coding: utf-8 -*-
import scrapy


class ResultsSpider(scrapy.Spider):
    name = "results"
    allowed_domains = ["173.255.199.232"]
    start_urls = (
        'http://173.255.199.232:8001/results/getresult',
    )

    def parse(self, response):
        pass
