#!/usr/bin/python
# -*- coding: utf-8 -*-


import os

# Selenium necesario para hacer click en el botón de showAll
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from awwa.items import AWWAItem


binary = FirefoxBinary('/usr/bin/iceweasel')

# Choose one to one to best define the serie
url = 'http://www.awwa.org/store/books.aspx'
# url = 'http://www.awwa.org/store/manuals.aspx'

if "manuals" in url:
    serie = "Manuals of water supply practices"
else:
    serie = ""


class AWWASpider(Spider):
    name = "awwa"
    allowed_domains = ["awwa.org"]

    def __init__(self, *args, **kwargs):
        super(AWWASpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

    def parse(self, response):
        driver = webdriver.Firefox(firefox_binary=binary)
        driver.get(response.url)
        driver.find_element_by_class_name("pagerShowAll").click()

        # Manual wait hasta que el usuario teclee una tecla para indicar que la
        # página ha terminado de cargar
        os.system("""bash -c 'read -s -n 1 -p "Press any key to continue when page load..."'""")
        print("\nContinue the loading")

        sites = driver.find_elements_by_class_name("ProductListItemControl")

        for site in sites:
            item = AWWAItem()
            url = site.find_element_by_xpath('a').get_attribute('href')
            item["url"] = url

            item["categories"] = ""

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

        item["serie"] = serie
        title = "".join(sel.xpath('.//span[@class="ProductDetailNameDisplay"]/text()').extract())
        number = 0
        if serie:
            try:
                number = int(title.split(" ")[0][1:])
                title = " ".join(title.split(" ")[1:])
            except ValueError:
                pass
        title = title.replace("(Print + PDF): ", "")
        title = title.replace("(Print + PDF) ", "")
        item["title"] = title
        item["number"] = number

        isbn = "".join(sel.xpath('.//span[@id="dnn_ctr10920_DNNWebControlContainer_ctl00_ProductINVInfoControl_AWWAProductDetailsCustomFields_isbnLabel"]/text()').extract())
        isbn = isbn.replace(" ", "")
        if not isbn:
            isbn = "ID-" + item["url"].split("=")[-1]
        item["isbn"] = isbn

        img = sel.xpath('.//img[@class="ProductDetailDisplayImage"]//@src').extract()[0]
        item["image"] = img
        item["imagehd"] = ""

        autor = "".join(sel.xpath('.//span[@id="dnn_ctr10920_DNNWebControlContainer_ctl00_ProductINVInfoControl_AWWAProductDetailsCustomFields_authorLabel"]/text()').extract())
        item["autor"] = autor

        date = "".join(sel.xpath('.//span[@id="dnn_ctr10920_DNNWebControlContainer_ctl00_ProductINVInfoControl_AWWAProductDetailsCustomFields_publicationDateLabel"]/text()').extract())
        item["date"] = date

        format = "".join(sel.xpath('.//span[@id="dnn_ctr10920_DNNWebControlContainer_ctl00_ProductINVInfoControl_AWWAProductDetailsCustomFields_mediaTypeLabel"]/text()').extract())
        count = "".join(sel.xpath('.//span[@id="dnn_ctr10920_DNNWebControlContainer_ctl00_ProductINVInfoControl_AWWAProductDetailsCustomFields_numberOfPageLabel"]/text()').extract())
        if format and count:
            pages = "%s, %s pag." % (format, count)
        elif format:
            pages = format
        elif count:
            pages = "%s pag." % count
        else:
            pages = ""
        item["pages"] = pages

        description = "".join(sel.xpath('.//div[@class="ProductDetailParagraphFullLabel"]/*').extract())
        item["description"] = description

        return item
