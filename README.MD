### Export environment variables

$ export $(grep -v '^#' .env | xargs)

scrapy crawl spider_name