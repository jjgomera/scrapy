# Scrapy settings for wiley project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'awwa'

SPIDER_MODULES = ['awwa.spiders']
NEWSPIDER_MODULE = 'awwa.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = ''

ITEM_PIPELINES = {
    'awwa.pipelines.AWWAPipeline': 300,
}
