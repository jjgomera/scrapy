#!/usr/bin/python
# -*- coding: utf-8 -*-


from lxml import html
import urllib2

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from packt.items import PacktItem


# Get initial count data
response = urllib2.urlopen('https://www.packtpub.com/all')
tree = html.fromstring(response.read())
text = tree.xpath('//div[@class="facet-cat-wrapper cf"]//div[@class="facet-cat-text"]/text()')[0]
count = int(text.split("(")[-1].split(")")[0])
print count
# Limitar count a los ultimos 500 libros una vez para actualizaciones de base
# de datos
count = 500

cat = {"application-development": "Application Development",
       "big-data-and-business-intelligence": "Big Data & Business Intelligence",
       "business": "Business",
       "game-development": "Game Development",
       "hardware-and-creative": "Hardware & Creative",
       "networking-and-servers": "Networking & Servers",
       "virtualization-and-cloud": "Virtualization & Cloud",
       "web-development": "Web Development"}


class PacktSpider(Spider):
    name = "packt"
    allowed_domains = ["www.packtpub.com"]

    def __init__(self, *args, **kwargs):
        super(PacktSpider, self).__init__(*args, **kwargs)
        pages = range(0, count, 48)
        self.start_urls = ["https://www.packtpub.com/all?search=&type_list[books]=books&offset=%i&rows=48&sort=sort_title+asc" % page for page in pages]

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="panel-panel panel-col-last"]//div[@class="book-block-outer"]')
        for indice, site in enumerate(sites):
            item = PacktItem()

            url2 = "".join(site.xpath(
                './/div[@class="book-block-overlay"]//a//@href').extract())
            item["url"] = "https://www.packtpub.com/"+url2
            category = url2.split("/")[1]

            try:
                item["categories"] = cat[category]
            except KeyError:
                item["categories"] = ""

            request = Request(item["url"], callback=self.parse2)
            request.meta['item'] = item
            yield request

    def parse2(self, response):
        item = response.meta['item']
        sel = Selector(response)

        item["title"] = sel.xpath('.//div[@class="book-top-block-info-title float-left"]//h1/text()').extract()[0]
        item['image'] = "http:"+"".join(sel.xpath(
            "//a[@class='fancybox']//@src").extract())
        item['imagehd'] = "https://www.packtpub.com" + \
            "".join(sel.xpath("//a[@class='fancybox']//@href").extract())
        autor = sel.xpath('.//div[@class="book-top-block-info-authors left"]//text()').extract()[0]
        autor = autor.replace("\n", "")
        autor = autor.replace("\t", "")
        item["autor"] = autor
        item["date"] = "".join(sel.xpath(
            './/time[@itemprop="datePublished"]//text()').extract())
        item['isbn'] = sel.xpath("//span[@itemprop='isbn']/text()").extract()[0]
        item['pages'] = sel.xpath("//div[@class='book-info-nb-page']//span[@class='label']/text()").extract()[0] + \
            " - "+sel.xpath("//span[@itemprop='numberOfPages']/text()").extract()[0] + " pages"

        description = "".join(sel.xpath(
            "//div[@class='book-info-about']/*").extract())
        description += "".join(sel.xpath(
            "//div[@class='book-info-audience']/*").extract())
        description += "".join(sel.xpath(
            "//div[@id='book-info-will-learn']/*").extract())
        description += "".join(sel.xpath(
            "//div[@class='book-info-bottom-indetail float-right']/*").extract())
        description += "".join(sel.xpath(
            "//div[@class='book-info-bottom-author float-right']/*").extract())
        item['description'] = description

        item["serie"] = ""
        item["quality"] = 0
        item["downloaded"] = False
        item["format"] = 0
        item["path"] = ""
        item["number"] = 0
        item["edition"] = ""
        return item
