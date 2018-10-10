# -*- coding: utf-8 -*-
import scrapy
from kuaishou.items import commentItem


class CommentSpider(scrapy.Spider):
    name = 'comment'
    allowed_domains = ['https://live.kuaishou.com']
    start_urls = ['http://https://live.kuaishou.com/u/WSQ_16888_dadong666/3xfeseu68r99bqk/']

    def parse(self, response):
        item = {}

        comments = response.xpath('/html/div[@"comment-item"]')
