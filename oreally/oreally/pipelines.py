# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from scrapy import log


class OreallyPipeline(object):

    def open_spider(self, spider):
        self.connection = sqlite3.connect('../book.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Oreilly \
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

        self.cursor2 = self.connection.cursor()
        self.cursor2.execute("""CREATE TABLE IF NOT EXISTS Starch \
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

        self.cursor3 = self.connection.cursor()
        self.cursor3.execute("""CREATE TABLE IF NOT EXISTS Maker \
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

        self.cursor4 = self.connection.cursor()
        self.cursor4.execute("""CREATE TABLE IF NOT EXISTS Pragmatic \
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
        if u"O'Reilly" in item["publisher"]:
            cursor = self.cursor
            table = "Oreilly"
        elif "Starch" in item["publisher"]:
            cursor = self.cursor2
            table = "Starch"
        elif "Maker" in item["publisher"]:
            cursor = self.cursor3
            table = "Maker"
        elif "Pragmatic" in item["publisher"]:
            cursor = self.cursor4
            table = "Pragmatic"
        else:
            print item["publisher"] + " Descartado " + item["title"]
            return

        cursor.execute(
            "select isbn from %s where isbn==?" % table, (item['isbn'], ))
        result = cursor.fetchone()
        if result:
            log.msg("Item already in database: %s" % item, level=log.DEBUG)
        else:
            cursor.execute(
                """insert into %s (url, title, autor, date, isbn, description,
                pages, serie, categories, image, imagehd, downloaded,
                format, quality, path, number, edition) values
                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""" % table,
                (item['url'], item['title'], item["autor"], item["date"],
                 item["isbn"], item["description"], item["pages"],
                 item["serie"], item["categories"], item["image"],
                 item["imagehd"], item["downloaded"], item["format"],
                 item["quality"], item["path"], item["number"],
                 item["edition"]))

            self.connection.commit()

            log.msg("Item stored : " % item, level=log.DEBUG)
            return item

    def handle_error(self, e):
        log.err(e)

    def close_spider(self, spider):
        self.connection.close()
