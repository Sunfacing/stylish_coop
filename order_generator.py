import random
import time
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


START_DATE = '2021-08-01'
END_DATE = '2021-09-30'


order_stat = [0, 1, 2, 3]
color_palette = [
    ["藍色", "007FFF"],
    ["綠色", "30D5C8"],
    ["紅色", "E32636"],
    ["灰色", "808080"],
    ["褐色", "704214"],
    ["黃色", "FFFDD0"],
    ["黑色", "000000"],
    ["白色", "FFFFFF"]
]

comment_list = [
    [1, '這裡買不到披薩'],
    [1, '聽說後端工程師有女朋友了(咬手帕)'],
    [2, '衣服被我撐破了'],
    [2, ''],
    [3, '還OK, 但我裸體更好看'],
    [3, '不好穿, 跟穿破布沒兩樣'],
    [3, '買了之後我天天被狗咬, 讓我經常衣不蔽體'],
    [3, '穿了這件後我的男朋友就不愛我了嗚嗚嗚'],
    [3, ''],
    [4, '品質不錯, 一定很多人買, 難怪我常跟別人撞衫'],
    [4, '媽祖跟我說一定要來這裡買衣服, 但我信耶穌'],
    [4, ''],
    [4, '衣服太好看, 害我老公以為我偷人, 怒扣1分'],
    [4, '聽說這網站的後端工程師很師, 求IG'],
    [4, '手機板特效好炫, 只能靠新台幣下架商品了'],
    [4, '只要是這裡推薦的都買啦, 哪次不買了'],
    [4, '品質很讚, 但還差我顏值一點'],
    [4, ''],
    [5, '網站怎麼能做得這麼漂亮, 一不小心就買了好幾件, 5分不能再高'],
    [5, '推薦商品我都好喜翻, 算命師都沒這麼準'],
    [5, '到貨速度堪比光速, 是找閃電俠送貨的嗎?'],
    [5, '穿上這件後我到哪都變成的焦點, 真是太棒惹'],
    [5, '自從我穿著這裡買的衣服打LOL後, 就再也沒輸過了'],
    [5, '材質摸起來很棒, 跟我的肌膚一樣'],
    [5, '很好穿, 已經無法再穿別家的衣服了'],
    [5, '']
]

def create_fake_user():
    user_list = []
    for i in range(1, 1000):
        role_id = 2
        provider = 'native'
        name = 'dummy{}'.format(i + 1)
        email = 'dummy{}@gmail.com'.format(i + 1)
        access_expired = 2592000
        user_list.append([role_id, provider, name, email, access_expired])
        query = "INSERT INTO user (role_id, provider, name, email, access_expired) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(query, user_list)
    print('fake_user created !!')


def get_all_user():
    cursor.execute("SELECT id FROM user")
    users = cursor.fetchall()
    return users


def query_all_sku_fa():
    query = "SELECT p.id AS product_id, v.id AS variant_id, p.category, p.subcat, p.title, p.price, v.size, c.code, c.name FROM stylish_coop.product AS p\
            INNER JOIN stylish_coop.variant AS v \
            ON v.product_id = p.id\
            INNER JOIN stylish_coop.color AS c\
            ON v.color_id = c.id\
            WHERE p.category IN ('women', 'accessories')"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def query_all_sku_ma():
    query = "SELECT p.id AS product_id, v.id AS variant_id, p.category, p.subcat, p.title, p.price, v.size, c.code, c.name FROM stylish_coop.product AS p\
            INNER JOIN stylish_coop.variant AS v \
            ON v.product_id = p.id\
            INNER JOIN stylish_coop.color AS c\
            ON v.color_id = c.id\
            WHERE p.category IN ('men', 'accessories')"
    cursor.execute(query)
    result = cursor.fetchall()
    return result

def str_time_prop(start, end, time_format, prop):
    """Get a time at a proportion of a range of two formatted times.

    start and end should be strings specifying times formatted in the
    given format (strftime-style), giving an interval [start, end].
    prop specifies how a proportion of the interval to be taken after
    start.  The returned time will be in the specified format.
    """
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)
    return time.strftime(time_format, time.localtime(ptime))

def random_date(start, end, prop):
    return str_time_prop(start, end, '%Y-%m-%d', prop)
    


def create_sales_record(gender_item_list, user_id_list, order_stat, comment_list):
    # Each user with preference has 1 - 4 orders during Aug - Sep
    u = 4
    order_table = []
    order_variant_table = []
    order_comment_table = []
    for user_id in user_id_list:
        user_id = user_id['id']
        shopping_times = random.randint(1, 4)
        
        # Each order has 1 ~ 6 items
        for i in range(shopping_times):
            date = random_date(START_DATE, END_DATE, random.random())
            # print(date)
            item_bought = random.randint(1, 6)
            order_date = date.replace('-', '')
            order_id = u

            # Set delivery status
            if date >= '2021-09-25':
                delivery_stat = random.choice(order_stat[:3])
            else:
                delivery_stat = order_stat[3]

            # Generate items
            ttl_amount = 0
            for item in range(item_bought):
                # Choose item randomly
                shopping_record = random.choice(gender_item_list)
                
                """Create record for order_variant"""
                order_variant = [order_id, shopping_record['title'], shopping_record['price'], shopping_record['size'], 1, shopping_record['code'], shopping_record['name'], shopping_record['variant_id']]
                order_variant_table.append(order_variant)

                """Create record for order_comment"""
                if delivery_stat == 3:
                    comment = random.choice(comment_list)
                    rating = comment[0]
                    comments = comment[1]
                    order_comment = [user_id, shopping_record['variant_id'], order_id, rating, comments]
                    order_comment_table.append(order_comment)
                    # print(order_comment)


                ttl_amount += shopping_record['price']

            """Create record for order_table"""
            # print(order_id)
            number = random.choice([0, 1, 2])
            order = [order_id, number, date, delivery_stat, user_id, ttl_amount, 60]
            order_table.append(order)
            # print(order)
            u += 1

    order_table_query = "INSERT INTO order_table(number, time, date, status, user_id, total, freight) VALUES (%s, %s, %s, %s, %s, %s)"
    order_variant_table_query = "INSERT INTO order_variant(order_id, name, price, size, qty, color_code, color_name, variant_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    order_comment_table_query = "INSERT INTO order_comments(user_id, variant_id, order_id, rating, comments) VALUES (%s, %s, %s, %s, %s)"
    cursor.executemany(order_table_query, order_table)
    cursor.executemany(order_variant_table_query, order_variant_table)    
    cursor.executemany(order_comment_table_query, order_comment_table)

    # print(order_table)
    # print(order_variant_table)
    # print(order_comment_table)
    

    # Create comment if delivery stat == '已送達'  -> use if to check then append
        # for time in range(time_bought):
        #     comment = random.choice(comment_lst)
        #     print(comment)







def main():
    # Create fake users
    # create_fake_user()

    # Select all users
    user_list = get_all_user()
    
    # Create category sku list by M/A, F/A
    ma_item_list = query_all_sku_ma()   
    fa_item_list = query_all_sku_fa()
    gender_list = [ma_item_list, fa_item_list]

    gender_preference = random.choices(gender_list, weights=(30, 70))
    # Create dummy data 

    # print(gender_preference)
    create_sales_record(gender_preference[0], user_list, order_stat, comment_list)



if __name__ == '__main__':
    main()








