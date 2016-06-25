# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import sqlite3
from scrapy import log


class OspreyPipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect('../bookOsprey.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Osprey \
                            (id INTEGER PRIMARY KEY,
                            url TEXT,
                            title TEXT,
                            image TEXT,
                            imagehd TEXT,
                            autor TEXT,
                            date TEXT,
                            isbn TEXT,
                            description TEXT,
                            pages TEXT,
                            serie TEXT,
                            categories TEXT,
                            downloaded BOOLEAN,
                            format INTEGER,
                            quality INTEGER,
                            path TEXT,
                            number INTEGER,
                            edition TEXT)""")

    def process_item(self, item, spider):
        self.cursor.execute(
            "select isbn from Osprey where isbn=?", (item['isbn'],))
        result = self.cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:
            self.cursor.execute(
                """insert into Osprey (url, title, autor, date, isbn,
                description, pages, serie, categories, image, imagehd,
                downloaded, format, quality, path, number, edition) values
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (item['url'], item['title'], item["autor"],
                 item["date"], item["isbn"], item["description"],
                 item["pages"], item["serie"], item["categories"],
                 item["image"], item["imagehd"], item["downloaded"],
                 item["format"], item["quality"], item["path"],
                 item["number"], item["edition"]))

            self.connection.commit()

            log.msg("Item stored : " % item, level=log.DEBUG)
            return item

    def handle_error(self, e):
        log.err(e)

    def close_spider(self, spider):
        self.connection.close()
