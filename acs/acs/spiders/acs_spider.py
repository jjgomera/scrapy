#!/usr/bin/python
# -*- coding: utf-8 -*-


from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from acs.items import ACSItem


# For better serie definiion run each serie at one
serie, yearStart, yearEnd = "symposium", 2010, 2016
# serie, yearStart, yearEnd = "advances", 1949, 1998


class ACSSpider(Spider):
    name = "acs"
    allowed_domains = ["pub.acs.org", "pubs.acs.org"]

    def __init__(self, *args, **kwargs):
        super(ACSSpider, self).__init__(*args, **kwargs)
        self.start_urls = []
        for year in range(yearStart, yearEnd+1):
            for page in range(1, 11):
                self.start_urls.append('http://pubs.acs.org/series/%s?seriesCode=%s&sortBy=Volume&startPage=%i&activeTab=Year&Year=%i' % (serie, serie, page, year))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="bookList"]/div[@class="bookBox"]')

        for site in sites:
            item = ACSItem()
            title = site.xpath('.//h2//a//text()').extract()[0]
            item["title"] = title
            url = site.xpath('.//h2//a//@href').extract()[0]
            item["url"] = "http://pubs.acs.org%s" % url
            img = site.xpath('.//img[@class="cover"]//@src').extract()[0]
            item["image"] = "http://pubs.acs.org" + img
            item["imagehd"] = ""

            if serie == "symposium":
                item["serie"] = "ACS Symposium"
            else:
                item["serie"] = "Advances in Chemistry"

            number = site.xpath('.//div[@class="meta1"]/div/text()').extract()[1]
            number = number.split()[-1]
            item["number"] = number

            autor = site.xpath('.//div[@class="meta1"]/div/text()').extract()[0]
            item["autor"] = autor
            date = site.xpath('.//div[@class="epubdate"]/text()').extract()[0]
            date = date.split(":")[-1]
            while date[0] == " ":
                date = date[1:]
            item["date"] = date

            isbn = site.xpath('.//div[@class="meta2"]/div/text()').extract()[0]
            isbn = isbn.split(":")[-1]
            while isbn[0] == " ":
                isbn = isbn[1:]
            item["isbn"] = isbn

            item["categories"] = ""

            item["pages"] = ""
            item["quality"] = 0
            item["downloaded"] = False
            item["format"] = 0
            item["path"] = ""
            item["edition"] = ""

            request = Request(item["url"], callback=self.parse2)
            request.meta['item'] = item
            yield request

    def parse2(self, response):
        item = response.meta['item']
        sel = Selector(response)

        description = "<h2>Table of contents</h2><br>"

        root = sel.xpath('.//div[@class="articleBox chapterBox"]')
        for child in root:
            chapter = ""
            chapter += child.xpath('.//div[@class="titleAndAuthor"]//h2//a/text()').extract()[0]
            autor = "".join(child.xpath('.//div[@class="titleAndAuthor"]//div[@class="articleAuthors"]/text()').extract())
            if autor and autor != item["autor"]:
                chapter += " (by %s)" % autor.title()
            info = child.xpath('.//div[@class="bookInfo"]//text()').extract()[0]
            if "Chapter" in info:
                capitulo = info.split(",")[0].split(" ")[-1]
                chapter = "%s - %s" % (capitulo, chapter)
            pages = info.split(",")[-1]
            chapter += pages
            description += chapter + "<br>"

        item["description"] = description

        return item
