# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html


from scrapy.item import Item, Field


class OspreyItem(Item):
    url = Field()
    title = Field()
    image = Field()
    imagehd = Field()
    autor = Field()
    date = Field()
    isbn = Field()
    description = Field()
    pages = Field()
    serie = Field()
    categories = Field()
    downloaded = Field()
    format = Field()
    quality = Field()
    path = Field()
    number = Field()
    edition = Field()
