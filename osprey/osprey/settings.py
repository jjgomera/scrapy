# Scrapy settings for crc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html


BOT_NAME = 'osprey'

SPIDER_MODULES = ['osprey.spiders']
NEWSPIDER_MODULE = 'osprey.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'osprey (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'osprey.pipelines.OspreyPipeline': 300,
}
