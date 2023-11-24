"""
This script is used to crawl data from various websites related to luxury handbags. It utilizes the crawl_url_list task from the tasks module.

Usage:
python3 -m luxeypipeline.main [-s SITE [SITE ...]]

Arguments:
-s SITE [SITE ...], --site SITE [SITE ...]
Specify the websites to crawl. If not provided, all websites will be crawled.

"""

from .tasks import crawl_url_list
import argparse
import random

site_config = {
    'mogi': {
        'start_urls': [
            'https://mogi.vn/mua-nha-dat?cp=[splash]'
        ],
        'start_page': 38200,
        'max_num_page': 39200,
    }, 
}

sites_list = ['mogi',
              ]

def get_url_with_page(site, page):
    return site_config[site]['start_urls'][0].replace('[splash]', str(page))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", nargs='+', help="input site")

    args = parser.parse_args()
    sites = args.site

    task_list = []
    for site in sites:
        for page in range(site_config[site]['start_page'], site_config[site]['max_num_page']):
            url = get_url_with_page(site, page)
            task_list.append((site, url, 'ddos', True))

    random.shuffle(task_list)
    for task_job in task_list:
        print(task_job)
        crawl_url_list.delay(
            task_job[0], task_job[1], task_job[2], task_job[3])


if __name__ == "__main__":
    main()
