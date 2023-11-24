### Setting up the Environment

1. This code can run only on linux. Use WSL if you on window.

2. Using python3.10

3. Fastest way to load environment variables from .env file:

```bash
export $(grep -v '^#' .env | xargs)
```

4. Import URLs to Redis:

```bash
python3 scripts/redis_init_urls.py
```

### Starting the Pipeline

1. Start the monitor:

```bash
celery -A property_crawler flower
```

2. Start the worker:

```bash
celery -A property_crawler worker -l info -Q crawl_list,crawl_item,io --purge -c 1

```

3. Run main script to start pipeline:

```bash
python3 -m property_crawler.main --mode full
```


### Stopping Waiting Tasks

If you need to stop waiting tasks, use the following command:

```bash
celery -A property_crawler purge -Q crawl_list,crawl_item,io

```
