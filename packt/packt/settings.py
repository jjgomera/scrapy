# Scrapy settings for crc project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html


BOT_NAME = 'packt'

SPIDER_MODULES = ['packt.spiders']
NEWSPIDER_MODULE = 'packt.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'packt (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'packt.pipelines.PacktPipeline': 300,
}
