import pymysql
import os
from dotenv import load_dotenv
import json



load_dotenv()

connection = pymysql.connect(
    host = os.getenv('host'),
    user = os.getenv('user'),
    passwd = os.getenv('passwd'),
    database = os.getenv('database'),
    port = int(os.getenv('port')),
    cursorclass = pymysql.cursors.DictCursor,
    autocommit=True
)
cursor = connection.cursor()




campaign = [
["210136", "https://obcdn4.obdesign.com.tw/images/ObdesignBanner/WOMEN/images/210914-BA6399_1920X820.jpg", "微秋 閨蜜穿搭"],
["210138", "https://obcdn4.obdesign.com.tw/images/ObdesignBanner/WOMEN/images/210928-DA8951-1920x820.jpg", "秋日女神 仙氣爆棚"],
["210137", "https://obcdn4.obdesign.com.tw/images/ObdesignBanner/WOMEN/images/210922-KG1221_1920X820.jpg", "休閒率性穿搭"]
]




def create_campaign(campaign):
    query = "INSERT INTO campaign (product_id, picture) VALUES (%s, %s)"
    query_lst = []
    for each in campaign:
       query_lst.append(each[:2])
    insert_query = "INSERT INTO campaign(product_id, picture) VALUES (%s, %s)"
    cursor.executemany(query_lst)
    print("create_campaign done")


def create_hot(campaign):
    hot_lst = []
    for each in campaign:
        campaign = each[2]
        hot_lst.append([campaign])
    query = "INSERT INTO hot(title) VALUES (%s)"
    cursor.executemany(query, hot_lst)
    print('create_hot_campaign done')

def create_hot_product(campaign):
    cursor.execute("SELECT * FROM hot")
    result = cursor.fetchall()
    query_lst = []
    for each in campaign:
        product_id = each[0]
        title = each[2]
        for hot in result:
            if hot['title'] == title:
                query_lst.append([hot['id'], int(product_id)])
    query = "INSERT INTO hot_product (hot_id, product_id) VALUES (%s, %s)"
    cursor.executemany(query, query_lst)
    print('create_hot_product done')


# create_hot(campaign)
# create_hot_product(campaign)
# create_campaign(campaign)