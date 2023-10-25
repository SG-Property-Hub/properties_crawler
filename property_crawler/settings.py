
BOT_NAME = "property_crawler"

SPIDER_MODULES = ["property_crawler.spiders"]
NEWSPIDER_MODULE = "property_crawler.spiders"


ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
   "property_crawler.pipelines.PropertyCrawlerPipeline": 300,
   "property_crawler.pipelines.LoadToDynamodbPipeline": 400,
}


SPLASH_URL = 'http://192.168.59.103:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"

LOG_LEVEL = 'INFO'