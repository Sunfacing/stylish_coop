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



with open('json/data.json', encoding='utf-8') as f:
    products = json.load(f)


def create_product(lst):
    product_lst = []
    for key, product in products.items():
        tmp_lst = [
            key,
            product['category'],
            product['title'],
            "厚薄：薄, 彈性：無",
            product['price'],
            product['texture'],
            product['wash'],
            product['place'],
            product['note'],
            product['story'],
            product['main_image'],
            product['subcat']
        ]
        product_lst.append(tmp_lst)
    query = "INSERT INTO product(id, category, title, description, price, texture, wash, place, note, story, main_image, subcat)\
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(query, product_lst)         
    print('products creation done')


def create_product_images(lst):
    product_lst = []
    for key, product in products.items():
        for img in product['img']:
            tmp_lst = [
                key, img 
            ]
            product_lst.append(tmp_lst)
    print('product_images creation done')


    query = "INSERT INTO product_images(product_id, image)\
            VALUES (%s, %s)"
    cursor.executemany(query, product_lst)    


def create_variant(lst):
    product_lst = []
    for key, product in products.items():
        colors = product['color'].strip().split(',')[:3]
        for color in colors:
            color = color.strip()
            if color == '白色':
                color_id = 1
            elif color == '綠色':
                color_id = 2
            elif color == '紅色':
                color_id = 3
            elif color == '灰色':
                color_id = 4
            elif color == '褐色':
                color_id = 5
            elif color == '黃色':
                color_id = 6
            elif color == '黑色':
                color_id = 7 
            elif color == '藍色':
                color_id = 8
            for size in product['size'].split(','):
                tmp_lst = [
                    key, int(color_id), size, product['stock']
                ]
                product_lst.append(tmp_lst)
    query = "INSERT INTO variant(product_id, color_id, size, stock)\
            VALUES (%s, %s, %s, %s)"
    cursor.executemany(query, product_lst) 
    print('variant creation done')


# create_product(products)
# create_product_images(products)
# create_variant(products)
