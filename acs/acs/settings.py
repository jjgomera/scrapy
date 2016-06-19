# Scrapy settings for wiley project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html


BOT_NAME = 'acs'

SPIDER_MODULES = ['acs.spiders']
NEWSPIDER_MODULE = 'acs.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'acs (+http://www.yourdomain.com)'

ITEM_PIPELINES = {
    'acs.pipelines.ACSPipeline': 300,
}
