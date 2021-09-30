from asyncio.tasks import sleep
import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import time
import random
import threading
from time import sleep
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pymongo import MongoClient
import os
from collections import defaultdict



load_dotenv()
mon_user = os.getenv('mon_user')
mon_pass = os.getenv('mon_pass')

client = MongoClient("mongodb+srv://{}:{}@cluster0.eryvt.mongodb.net/AppWorks".format(mon_user, mon_pass))
db = client.AppWorks
collection = db.cooperation
collection2 = db.url_for_crawler



# sub = collection2.find({})
# subgroup_list = []
# for each in sub:
#     for url in each['url'][:15]:
#         subgroup_list.append([each['subgroup'], url])

# print(subgroup_list)


# category_url_scrape
top_f = 'https://www.obdesign.com.tw/inpage.aspx?no=6987'
atm_f = 'https://www.obdesign.com.tw/inpage.aspx?no=11252'
btm_f = 'https://www.obdesign.com.tw/inpage.aspx?no=7007'
coat_f = 'https://www.obdesign.com.tw/inpage.aspx?no=7001'
dress_f = 'https://www.obdesign.com.tw/inpage.aspx?no=6995'
atm_m = 'https://www.obdesign.com.tw/inpage.aspx?no=122991'
top_m = 'https://www.obdesign.com.tw/inpage.aspx?no=7032'
btm_m = 'https://www.obdesign.com.tw/inpage.aspx?no=159363'
coat_m = 'https://www.obdesign.com.tw/inpage.aspx?no=7033'
acc = 'https://www.obdesign.com.tw/inpage.aspx?no=7014'





options = Options()
options.add_argument("--disable-notifications")
chrome = webdriver.Chrome('./chromedriver', chrome_options=options)







# Collect item list
subgroups = [
    ['top_f', top_f],
    ['atm_f', atm_f],
    ['btm_f', btm_f],
    ['coat_f', coat_f],    
    ['dress_f', dress_f],
    ['atm_m', atm_m],
    ['top_m', top_m],
    ['btm_m', btm_m],
    ['coat_m', coat_m],
    ['acc', acc]
]



# get single product link from category main page
def get_product_url(subgroup):
    url = subgroup[1]
    subgroup = subgroup[0]
    urls = []
    chrome.get(url)
    for x in range(1, 4):
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    links = soup.find_all('a')
    for link in links:
        if link.has_attr('href') and 'https://www.obdesign.com.tw/product' in link['href']:
            urls.append(link['href'])
            print(link['href'])
    chrome.quit()
    record = {'subgroup': subgroup, 'url': urls}
    collection2.insert_one(record)
    # print(collection2.find_one({}))



# get product url automatically
def get_single_product_from_cate_page(subgroups):
    for i in range(len(subgroups)):
        if i > 9:
            y = get_product_url(subgroups[i])
            sleep(3)



# Full Crawler process
def crawler(subgroup, url):
    chrome.get(url)
    for x in range(1, 4):
        chrome.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(2)

    # Get title 
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    title = soup.find('h1').getText()
    # print(title)

    # Get origin/texture
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    origin = soup.find_all('div', {'class': "content_td"})
    ori_text = []
    for each in origin:
        ori_text.append(each.getText())
        # print(each.getText())

    # Get Color
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    color = soup.find('div', {'class': "sku-color-name subtitle"}).getText()[3:]
    # print(color)

    # Get Story
    soup = BeautifulSoup(chrome.page_source, 'html.parser')
    desc = soup.find('div', {'class': 'desc'}).getText()
    # print(desc)

    imgs = soup.find_all('img')
    images = []
    for img in imgs:
        if 'PIC' in img['src'] or 'CB-1-1' in img['src']:
            images.append(img['src'])
            # print(img['src'])

    diction = defaultdict(dict)

    product = {'title': title, 
                'color': color, 
                'desc': desc, 
                'ori_text': ori_text, 
                'images': images,
                'subgroup': subgroup }
    # print(product)
    x = collection.insert_one(product)
    chrome.quit()
    return product



# images downloader
def get_image(url,name,num):
    response = requests. get(url)
    file = open(name+str(num)+".jpg", "wb")
    file. write(response. content)
    file.close()



new = [
['btm_f', "https://www.obdesign.com.tw/product.aspx?seriesID=KG1221-&no=7010&cbv=7010-117128-52023-684469-B2&color=%E8%BB%8D%E7%B6%A0/%E5%A5%B6%E8%8C%B6"],
['btm_f',"https://www.obdesign.com.tw/product.aspx?seriesID=BA6399-&no=11321&cbv=11321-145799-49089-681890-B1&color=%E6%B7%B1%E7%81%B0"],
['dress_f', 'https://www.obdesign.com.tw/product.aspx?seriesID=DA8951-&no=11252&cbv=11252-158012-51446-685434-B3_1&color=%E7%99%BD']
]


def single_item_scrape(n, lst):
    for subgroup in lst[n:n+1]:
        try:
            print(subgroup)
            result = crawler(subgroup[0], subgroup[1])
            x = collection.insert_one(result)
            sleep(5)
        except:
            print('error')


# def task(subgroup_list):
#     for subgroup in subgroup_list:
#         task = threading.Thread (target=crawler, args=((subgroup[0], subgroup[1] )))
#         print('task starts', subgroup)
#         sleep(1)
#         task.start()
#     task.join()
    

# task(subgroup_list)

   


# if __name__ == "__main__":
    # url = 'https://www.obdesign.com.tw/product.aspx?seriesID=BA6381-&no=11088&gclid=CjwKCAjw-sqKBhBjEiwAVaQ9a6NiG62gDgrOWGrhywGKOGxZw5al5vhtquUkd_MtQCYyCya_klK0gBoCxS4QAvD_BwE&cbv=11088-103534-53148-0-E2'
    # crawler(url)
    # for i in range(10):
    #     task(scrap_lst) 
