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

site_urls = {
    'mogi': [
        'https://mogi.vn/mua-nha-dat'
    ],
    'bds68':[
        'https://bds68.com.vn/nha-dat-ban?pg=1'
    ],
    'muaban':[
        'https://muaban.net/listing/v1/classifieds/listing?subcategory_id=169&category_id=33&limit=20&offset=0'
    ],
    'nhatot':[
        'https://gateway.chotot.com/v1/public/ad-listing?st=s,k&limit=100&o=0&cg=1000&region_v2=13000&area_v2=13119&key_param_included=true'   
    ],
    'batdongsan_so':[
        'https://batdongsan.so/api/v1/home/demand/1/posts?page=1'
    ],
    'ibatdongsan':[
        'https://i-batdongsan.com/can-ban-nha-dat.htm'
    ],
    'batdongsanonline':[
        'https://batdongsanonline.vn/mua-ban-dat/?page=1'
    ],
    'bds123':[
        'https://bds123.vn/nha-dat-ban.html?page=1'
    ],
    'w123nhadatviet':[
        'https://123nhadatviet.com/rao-vat/can-ban/nha-dat.html'
    ],
    'nhadat24h':[
        'https://nhadat24h.net/nha-dat-ban/page1'
    ],
    'houseviet':[
        'https://houseviet.vn/nha-dat-ban'
    ]
}

sites_list = ['mogi', 'bds68', 'muaban', 'nhatot', 'batdongsan_so', 'ibatdongsan'
            ]
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--site", nargs='+', help="input site")
    parser.add_argument("-e", "--exclude", nargs='+', help="input excluded site")
    # Mode: basic, full
    parser.add_argument("-m", "--mode", type = str, default = "basic", help="input mode")
    # Crawl only
    parser.add_argument("-lc", "--save_local", action='store_true', default=False, help="boolean save to local parameter")
    parser.add_argument("-rf", "--read_file", action='store_true', default=False, help="boolean read_file parameter")

    args = parser.parse_args()
    sites = args.site
    excluded_sites = args.exclude
    mode = args.mode
    save_local = args.save_local
    read_file = args.read_file
    
    if read_file:
        crawl_url_list.delay()
        return
    # If no sites provided, update all sites
    if sites is None:
        sites = sites_list

    # Remove excluded sites from the list
    if excluded_sites:
        sites = list(set(sites) - set(excluded_sites))

    task_list = []
    for site in sites:
        for url in site_urls[site]:
            print(site, url, mode, 'save to local' if save_local else 'save to mongodb')
            task_list.append((site, url, mode, save_local))

    #shuffle task list
    random.shuffle(task_list)
    for task_job in task_list:
        print(task_job)
        crawl_url_list.delay(task_job[0], task_job[1], task_job[2], task_job[3])

if __name__ == "__main__":
    main()