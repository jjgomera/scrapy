# Scrapy settings for crc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'oreally'

SPIDER_MODULES = ['oreally.spiders']
NEWSPIDER_MODULE = 'oreally.spiders'

# Added to avoid banned
DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:10.0.1) Gecko/20100101 Firefox/10.0.1'

ITEM_PIPELINES = {
    'oreally.pipelines.OreallyPipeline': 300,
}
