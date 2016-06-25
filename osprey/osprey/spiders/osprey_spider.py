#!/usr/bin/python
# -*- coding: utf-8 -*-


from lxml import html
import urllib2

from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector

from osprey.items import OspreyItem


# Get initial count data
response = urllib2.urlopen('https://ospreypublishing.com/store')
tree = html.fromstring(response.read())
count = int(tree.xpath('//p[@class="amount"]/text()')[0].split(" ")[-2])
# Limitar count a los ultimos 500 libros una vez para actualizaciones de base
# de datos
# count = 5
print count


class OspreySpider(Spider):
    name = "osprey"
    allowed_domains = ["ospreypublishing.com"]

    def __init__(self, *args, **kwargs):
        super(OspreySpider, self).__init__(*args, **kwargs)
        pages = count//24 + 1
        self.start_urls = []
        for page in range(1, pages+1):
            self.start_urls.append(
                "https://ospreypublishing.com/store?limit=24&p=%i" % page)

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//div[@class="item-inner"]')
        for indice, site in enumerate(sites):
            item = OspreyItem()

            url = site.xpath('./a//@href').extract()[0]
            if "contributor" not in url:
                item["url"] = url

                request = Request(item["url"], callback=self.parse2)
                request.meta['item'] = item
                yield request

    def parse2(self, response):
        item = response.meta['item']
        sel = Selector(response)

        item['image'] = sel.xpath("//img[@id='image']//@src").extract()[0]
        item['imagehd'] = ""

        item["autor"] = ""
        item["date"] = ""
        isbn = ""
        format = ""
        pages = ""
        data = sel.xpath('.//ul[@class="additional-data"]//li')
        for dat in data:
            txt = "".join(
                dat.xpath('.//span[@class="data-label"]/text()').extract())
            if "Author" in txt:
                autor = "".join(dat.xpath('.//strong/text()').extract())
                item["autor"] = autor
            elif "Illustrator" in txt:
                ilustrador = "".join(dat.xpath('.//strong/text()').extract())
                item["autor"] += " (Ilustrador: %s)" % ilustrador
            elif "ISBN" in txt:
                isbn = "".join(dat.xpath('.//strong/text()').extract())
            elif "Publication Date" in txt:
                date = "".join(dat.xpath('.//strong/text()').extract())
                item["date"] = date
            elif "Format" in txt:
                format = "".join(dat.xpath('.//strong/text()').extract())
            elif "Number of Pages" in txt:
                pages = "".join(dat.xpath('.//strong/text()').extract())
                pages += " Pags."

        if not isbn:
            try:
                isbn = item["image"].split("_")[-2].split("/")[-1]
                int(isbn)
            except IndexError:
                isbn = item["url"].split("/")[-1]
            except ValueError:
                isbn = item["url"].split("/")[-1]
            if not isbn:
                isbn = item["url"]
        item["isbn"] = isbn

        lst = []
        for data in (format, pages):
            if data:
                lst.append(data)
        txt = ", ".join(lst)
        if txt:
            item["pages"] = txt
        else:
            item["pages"] = ""

        title = "".join(
            sel.xpath('.//div[@class="product-name"]//h1/text()').extract())
        subtitle = "".join(sel.xpath(
            './/div[@class="product-subtitle"]//h2/text()').extract())
        if subtitle:
            title += ": " + subtitle
        item["title"] = title
        serie = sel.xpath('.//div[@class="product-code"]/text()').extract()[0]
        serie = serie.replace("\t", "")
        serie = serie.replace("\n", "")
        while serie and serie[-1] == " ":
            serie = serie[:-1]

        try:
            num = int(serie.split(" ")[-1])
            serie = " ".join(serie.split(" ")[:-1])
        except ValueError:
            num = 0
        item["serie"] = serie
        item["number"] = num

        description = "".join(sel.xpath(
            './/div[@class="box-collateral box-description"]/*').extract())
        item['description'] = description

        item["categories"] = ""
        item["quality"] = 0
        item["downloaded"] = False
        item["format"] = 0
        item["path"] = ""
        item["edition"] = ""
        return item
