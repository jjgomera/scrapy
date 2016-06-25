#!/usr/bin/python
# -*- coding: utf-8 -*-


import urllib2
from lxml import html

from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

from oreally.items import OreillyItem

cate = {
    "apple-mac": "Apple",
#    "apple-mac/apple-apps": "Apple:/Apple Apps",
#    "apple-mac/apple-programming": "Apple:/Apple Programming",
#    "apple-mac/ios-programming": "Apple:/iOS Programming",
#    "apple-mac/ipad-iphone-ipod": "Apple:/iPad, iPhone, & iPod",
#    "apple-mac/mac": "Apple:/Mac",

    "apps-software": "Apps & Software",
#    "apps-software/apple-apps": "Apps & Software:/Apple Apps",
#    "apps-software/design-apps": "Apps & Software:/Design Apps",
#    "apps-software/office-sharepoint": "Apps & Software:/Office & SharePoint",
#    "apps-software/photo-apps": "Apps & Software:/Photoshop & Photo Apps",
#    "apps-software/web-mobile-apps": "Apps & Software:/Web & Mobile Apps",

    "digital-audio-video": "Audio & Video",
#    "digital-audio-video/digital-audio": "Audio & Video:/Audio",
#    "digital-audio-video/digital-video": "Audio & Video:/Video",

    "business": "Business",
#    "business/accounting-finance": "Business:/Accounting & Finance",
#    "business/agile": "Business:/Agile & Lean",
#    "business/business-management": "Business:/Business Management & Leadership",
#    "business/career-development": "Business:/Career Development",
#    "business/entrepreneurship": "Business:/Entrepreneurship",
#    "business/it-leadership": "Business:/IT Leadership",
#    "business/project-management": "Business:/Project Management",
#    "business/sales-marketing": "Business:/Sales & Marketing",
#    "business/society-culture": "Business:/Society & Culture",

    "certification-training": "Certification",
#    "certification-training/cisco-certification": "Certification:/Cisco Certification",
#    "certification-training/linux-certification": "Certification:/Linux Certification",
#    "certification-training/microsoft-certification-training": "Certification:/Microsoft Certification & Training",
#    "certification-training/pmp": "Certification:/PMP",
#    "certification-training/other-certification": "Certification:/Other Certification",

    "data": "Data",
#    "data/data-analysis-visualization": "Data:/Data Analysis & Visualization",
#    "data/data-topics": "Data:/Data Topics",
#    "data/non-relational-databases": "Data:/Non-Relational Databases",
#    "data/sas": "Data:/SAS",
#    "data/oracle": "Data:/Oracle",
#    "data/relational-databases": "Data:/Relational Databases",
#    "data/sql-server": "Data:/SQL Server",

    "design": "Design",
#    "design/animation": "Design:/Animation",
#    "design/design-apps": "Design:/Design Apps",
#    "design/digital-publishing": "Design:/Digital Publishing",
#    "design/game-design": "Design:/Game Design & Development",
#    "design/information-architecture": "Design:/Information Architecture",
#    "design/mobile-design": "Design:/Mobile Design & Development",
#    "design/prod-design": "Design:/Product Design",
#    "design/user-experience": "Design:/User Experience",
#    "design/web-design": "Design:/Web Design",

    "science-math": "Engineering, Math, & Science",
#    "science-math/bioinformatics": "Engineering, Math, & Science:/Bioinformatics",
#    "science-math/electrical-engineering": "Engineering, Math, & Science:/Electrical Engineering",
#    "science-math/hardware-engineering": "Engineering, Math, & Science:/Hardware Engineering",
#    "science-math/math": "Engineering, Math, & Science:/Math",
#    "science-math/science": "Engineering, Math, & Science:/Science",

    "health": "Health & Wellness",
#    "health/cancer": "Health & Wellness:/Cancer",
#    "health/disorders-diseases": "Health & Wellness:/Disorders & Diseases",
#    "health/health-it": "Health & Wellness:/Health IT",
#    "health/mind-body": "Health & Wellness:/Mind & Body",

    "iot": "IoT (Internet of Things)",
#    "iot/diy-projects": "IoT:/DIY Projects",
#    "iot/electronics": "IoT:/Electronics",
#    "iot/hardware-hacking": "IoT:/Hardware Hacking",
#    "iot/lego-robotics": "IoT:/Lego & Robotics",
#    "iot/make-craft": "IoT:/Make & Craft",

    "microsoft": "Microsoft",
#    "microsoft/dotnet": "Microsoft:/.NET & Windows Programming",
#    "microsoft/business-solutions": "Microsoft:/Microsoft Business Solutions",
#    "microsoft/certification-training": "Microsoft:/Microsoft Certification & Training",
#    "microsoft/servers": "Microsoft:/Microsoft Servers",
#    "microsoft/software-development": "Microsoft:/Microsoft Software Development",
#    "microsoft/webdesign": "Microsoft:/Microsoft Web Design & Development",
#    "microsoft/office-sharepoint": "Microsoft:/Office & Sharepoint",
#    "microsoft/windows": "Microsoft:/Windows",
#    "microsoft/windows-administration": "Microsoft:/Windows Administration",
#    "microsoft/windows-phone": "Microsoft:/Windows Phone",
#    "microsoft/windows-phone-programming": "Microsoft:/Windows Phone Programming",

    "mobile-devices": "Mobile & Ereader Devices",
#    "mobile-devices/android": "Mobile & Ereader Devices:/Android",
#    "mobile-devices/ipad-iphone-ipod": "Mobile & Ereader Devices:/iPad, iPhone, & iPad",
#    "mobile-devices/kindle": "Mobile & Ereader Devices:/Kindle",
#    "mobile-devices/nook": "Mobile & Ereader Devices:/Nook",
#    "mobile-devices/windows-phone": "Mobile & Ereader Devices:/Windows Phone",
#    "mobile-devices/other-devices": "Mobile & Ereader Devices:/Other Devices",

    "networking": "Networking",
#    "networking/cisco": "Networking:/Cisco",
#    "networking/cloud-network-security": "Networking:/Cloud & Network Security",
#    "networking/home-networking": "Networking:/Home Networking",
#    "networking/network-administration": "Networking:/Network Administration",
#    "networking/networking-topics": "Networking:/Networking Topics",

    "personal-computing": "Personal Computing",
#    "personal-computing/home-networking": "Personal Computing:/Home Networking",
#    "personal-computing/mac": "Personal Computing:/Mac",
#    "personal-computing/pc": "Personal Computing:/PC",
#    "personal-computing/windows": "Personal Computing:/Windows",

    "personal-growth": "Personal Growth",
#    "personal-growth/business-management-leadership": "Personal Growth:/Business Management & Leadership",
#    "personal-growth/career-development": "Personal Growth:/Career Development",
#    "personal-growth/mind-body": "Personal Growth:/Mind & Body",
#    "personal-growth/personal-finance": "Personal Growth:/Personal Finance",

    "digital-photography": "Photography",
#    "digital-photography/camera-guides": "Photography:/Camera Guides",
#    "digital-photography/digital-photography": "Photography:/Digital Photography",
#    "digital-photography/photoshop": "Photography:/Photoshop & Photo Apps",

    "programming": "Programming",
#    "programming/dotnet": "Programming:/.NET & Windows",
#    "programming/agile": "Programming:/Agile",
#    "programming/android-programming": "Programming:/Android",
#    "programming/apple-programming": "Programming:/Apple",
#    "programming/c": "Programming:/C/C++",
#    "programming/csharp": "Programming:/C#",
#    "programming/design-patterns": "Programming:/Design Patterns",
#    "programming/game-design": "Programming:/Game Design & Development",
#    "programming/graphics-multimedia-programming": "Programming:/Graphics & Multimedia",
#    "programming/ios-programming": "Programming:/iOS",
#    "programming/java": "Programming:/Java",
#    "programming/javascript": "Programming:/JavaScript",
#    "programming/perl": "Programming:/Perl",
#    "programming/mobile-design": "Programming:/Mobile Design & Development",
#    "programming/php": "Programming:/PHP",
#    "programming/python": "Programming:/Python",
#    "programming/r": "Programming:/R",
#    "programming/ruby": "Programming:/Ruby & Rails",
#    "programming/secure-programming": "Programming:/Secure",
#    "programming/software-engineering": "Programming:/Software Engineering",
#    "programming/testing": "Programming:/Testing",
#    "programming/windows-phone-programming": "Programming:/Windows Phone",
#    "programming/other-programming-languages": "Programming:/Other Languages",

    "security": "Security & Cryptography",
#    "security/cloud-network-security": "Security & Cryptography:/Cloud & Network Security",
#    "security/computer-security": "Security & Cryptography:/Computer Security",
#    "security/cryptography": "Security & Cryptography:/Cryptography",
#    "security/secure-programming": "Security & Cryptography:/Secure Programming",

    "system-administration": "System Administration",
#    "system-administration/cloud-administration": "System Administration:/Cloud Administration",
#    "system-administration/email-administration": "System Administration:/Email Administration",
#    "system-administration/linux-unix": "System Administration:/Linux & Unix",
#    "system-administration/microsoft-servers": "System Administration:/Microsoft Servers",
#    "system-administration/performance": "System Administration:/Performance",
#    "system-administration/system-admin-ops": "System Administration:/System Admin & Ops",
#    "system-administration/windows-administration": "System Administration:/Windows Administration",

    "tech-culture": "Tech Culture",
#    "tech-culture/game-strategy": "Tech Culture:/Game Strategy",
#    "tech-culture/tech-culture": "Tech Culture:/Tech Culture",

    "web-development": "Web Development",
#    "web-development/html-css": "Web Development:/HTML & CSS",
#    "web-development/javascript": "Web Development:/JavaScript",
#    "web-development/performance": "Web Development:/Performance",
#    "web-development/php": "Web Development:/PHP",
#    "web-development/ruby-rails": "Web Development:/Ruby & Rails",
#    "web-development/sem-seo": "Web Development:/SEM & SEO",
#    "web-development/web-content-management": "Web Development:/Web Content Management",
#    "web-development/web-design": "Web Development:/Web Design",
#    "web-development/web-development": "Web Development:/Web Development"
    }

categories = cate.keys()

# Get initial count data
count = []
for cat in categories:
#    response = urllib2.urlopen('http://shop.oreilly.com/category/browse-subjects/%s.do?sortby=publicationDate&page=1' % cat)
#    tree = html.fromstring(response.read())
#    try:
#        num = tree.xpath('//td[@class="default"]//option/@value')[-1].split("=")[-1]
#    except IndexError:
#        num = 1
#    count.append(int(num))
    num = 1
    count.append(1)
    print num, cat


class OreallySpider(Spider):
    name = "oreally"
    allowed_domains = ["shop.oreilly.com"]

    def __init__(self, *args, **kwargs):
        super(OreallySpider, self).__init__(*args, **kwargs)

        self.start_urls = []
        for cat, num in zip(categories, count):
            for page in range(1, num+1):
                self.start_urls.append("http://shop.oreilly.com/category/browse-subjects/%s.do?sortby=publicationDate&page=%i" %(cat, page))

    def parse(self, response):
        sel = Selector(response)
        sites = sel.xpath('//td[@class="thumbtext"]')
        for indice, site in enumerate(sites):
            item = OreillyItem()

            url = "".join(site.xpath(
                './/div[@class="thumbcontainer"]//div[@class="thumbdiv"]//a//@href').extract())
            item["url"] = "http://shop.oreilly.com"+url
            isbn = url.split("/")[-1].split(".")[0]
            item['isbn'] = isbn
            category = response.request.url.split("browse-subjects/")[-1].split(".do")[0]
            item["categories"] = cate[category]

            request = Request(item["url"], callback=self.parse2)
            request.meta['item'] = item
            yield request

    def parse2(self, response):
        item = response.meta['item']
        sel = Selector(response)
        format = "".join(sel.xpath(
            "//meta[@name='Category']/@content").extract())
        if format == "Video":
            print "Video descartado"
            return
        title = "".join(sel.xpath(
            "//meta[@name='book_title']/@content").extract())
        title2 = "".join(sel.xpath(
            "//meta[@name='subtitle']/@content").extract())
        if title2:
            title += ": " + title2
        item['title'] = title
        item['autor'] = "".join(sel.xpath(
            "//meta[@name='author']/@content").extract())
        item['date'] = "".join(sel.xpath(
            "//meta[@name='search_date']/@content").extract())
        item['image'] = "".join(sel.xpath(
            "//meta[@name='graphic_large']/@content").extract())

        hasLargeImage = sel.xpath("//div[@class='viewLarger']/a").extract()
        if hasLargeImage:
            imagehd = item['image'].replace("cat", "lrg")
            imagehd = imagehd.replace("gif", "jpg")
        else:
            imagehd = ""
        item["imagehd"] = imagehd

        item['publisher'] = "".join(sel.xpath(
            "//meta[@name='publisher']/@content").extract())
        item['pages'] = "".join(sel.xpath(
            "//div[@class='default']/text()").extract())
        description = "".join(sel.xpath(
            "//div[@class='detail-description-content']/*").extract())

        if not description:
            description = "".join(sel.xpath(
                "//div[@style='margin: 12px 0 10px 190px; overflow: auto;']//p/text()").extract())
        item['description'] = description

        item["serie"] = ""
        item["quality"] = 0
        item["downloaded"] = False
        item["format"] = 0
        item["path"] = ""
        item["number"] = 0
        item["edition"] = ""
        return item
