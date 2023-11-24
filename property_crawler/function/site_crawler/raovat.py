import requests
import re
from datetime import datetime
import logging
import json
import time
# from property_crawler.items import PropertyCrawlerItem
from decimal import Decimal
from bs4 import BeautifulSoup

def raovat_list(url = None):

    crawl_url ="https://raovat.vnexpress.net/tp-ho-chi-minh/huyen-binh-chanh/mua-ban-nha-dat?page=1"
    if url:
        crawl_url=url
        
    region = crawl_url.split(".net/")[1].split("/")
    city = region[0]
    city_list = [key for item in geodata for key in item.keys()]
    city_index = city_list.index(city)

    dist = region[1]
    dist_list= geodata[city_index][city]
    dist_index= dist_list.index(dist)
    
    res = requests.get(crawl_url)
    soup = BeautifulSoup(res.text,"html.parser")
    products =soup.find("div",class_="list-item-post").find_all("div",class_="item-post")

    if len(products) >0:
        urls=[]
        for product in products:
            url = 'https://raovat.vnexpress.net'+ product.find("a")["href"]
            urls.append(url)
    
        num_cur_page = int(crawl_url.split("page=")[1])
        next_page = "https://raovat.vnexpress.net/{}/{}/mua-ban-nha-dat?page=".format(city,dist) + str(num_cur_page + 1)
        return {'urls': urls, 'next_page': next_page}
    else:
        with open('/home/etsu_daemon/project/property-crawler/property_crawler/function/site_crawler/input_data/homedy.json') as json_file:
            geodata = json.load(json_file)
        city_list = [key for item in geodata for key in item.keys()]
        city_index = city_list.index(city)
        dist_list= geodata[city_index][city]
        dist_index= dist_list.index(dist)
        if dist_index == len(dist_list)-1:
            dist_index = -1
            city_index+=1
            city = city_list[city_index]
        dist_list= geodata[city_index][city]
        dist =dist_list[dist_index+1]
        next_page = "https://raovat.vnexpress.net/{}/{}/mua-ban-nha-dat?page=1".format(city,dist)
        return {'urls': [], 'next_page': next_page}

def convert_price(price):
    list_price = price.split(" ")
    if list_price[1] == 'VNĐ':
        sum_price =list_price[0].replace(".","")
    else:
        sum_price = 0
        for i in range(len(list_price)):
            if list_price[i] == "tỷ":
                sum_price+= float(list_price[i-1].replace(",",".")) * (10**9)
            elif list_price[i] == "triệu":
                sum_price+= float(list_price[i-1].replace(",",".")) * (10**6)
    return int(sum_price)

def convert_address_info(address):
     #full string_format : "10 ngõ 55, Đường Lê Quý Đôn, Phường Bạch Đằng, Quận Hai Bà Trưng, Hà Nội"
     # convert to address,city,dist,ward,street
    info = {}
    info["address"] = address
    list_info = address.split(", ")
    list_loc = ["city","dist","ward","street"]
    for i in range(len(list_loc)):
        if len(list_info) - i -1 >= 0 :
            info[list_loc[i]] = list_info[len(list_info) - i -1].strip()
    return info

def raovat_item(url):
    
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    item ={}
    
    title = soup.find("h1",class_="title-detail").get_text()
    item["title"]=title
    
    item['site'] = 'raovat'
    item["url"] = res.url
    
    price_string = soup.find("span",class_="price-current-value").get_text()
    if price_string == 'Thỏa thuận':
        item["price_string"] = price_string
    else:
        price = convert_price(price_string)
        item["price"] = price
        item["price_string"]=price_string
    
    image_list = []  
    images = soup.find("div",class_="swiper-post-detail clearfix").find_all("img")
    for image in images:
        image_list.append(image["src"])
    
    item["images"]=image_list
    
    item["description"]= soup.find("div",class_="content-detail js-content").get_text().strip()
    
    item["property_type"] = soup.find_all("li",class_="breadcrumb-item")[3].get_text().strip()
    
    date_list = soup.find("p",class_="info-posting-time").get_text().split(", ")
    date_string = date_list[1]+ ' '+date_list[2].split(" ")[0]
    date = datetime.strptime(date_string, "%d/%m/%Y %H:%M").strftime("%Y-%m-%d %H:%M:%S")
    item["publish_at"] = date
    
    address = soup.find("p",class_="info-location").get_text().split(": ")[1]
    item["location"] = convert_address_info(address)
    
    try:
        main_info = {}
        main_info_string = soup.find_all("li",class_="item-attribute")
        for i in main_info_string:
            temp = i.find_all("span")
            main_info[temp[0].get_text().strip()] = temp[1].get_text().strip()
        
        item["attr"] = {}
    
        if 'Diện tích căn hộ(m²):' in main_info:
            item["attr"]["area"] = float(main_info["Diện tích căn hộ(m²):"].replace(",","."))
            item["attr"]["total_area"] = float(main_info["Diện tích căn hộ(m²):"].replace(",","."))
        
        if 'Giấy tờ pháp lý:' in main_info:
            item["attr"]["certificate"] = main_info["Giấy tờ pháp lý:"]
            
        if 'Hướng nhà:' in main_info:
            item["attr"]["direction"] = main_info["Hướng nhà:"]
        
        if 'Phòng tắm:' in main_info:
            item["attr"]["bathroom"] = int(main_info["Phòng tắm:"])
        
        if 'Phòng ngủ:' in main_info:
            item["attr"]["bedroom"] = main_info["Phòng ngủ:"]
        
    except Exception as e:
        print('Error when parse attr', e)
        pass
        
    item["agent"] = {}
    try:
        name = soup.find("p",class_="info-item").find("a").get_text()
        item["agent"]["name"]=name
    except:
        pass
    try:
        profile = soup.find("p",class_="info-item").find("a")["href"]
        item["agent"]["profile"] =' https://raovat.vnexpress.net' + profile
    except:
        pass
    
    return items