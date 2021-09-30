import os
from pymongo import MongoClient
from dotenv import load_dotenv
from collections import defaultdict
import random
import json




load_dotenv()
mon_user = os.getenv('mon_user')
mon_pass = os.getenv('mon_pass')

client = MongoClient("mongodb+srv://{}:{}@cluster0.eryvt.mongodb.net/AppWorks?tls=true&tlsAllowInvalidCertificates=true".format(mon_user, mon_pass))
db = client.AppWorks
collection2 = db.cooperation

new_collection = defaultdict(dict)
data = collection2.find({})



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

   

category ={
    'top_f': ['women', 'topwear'],
    'btm_f': ['women', 'bottomwear'],
    'atm_f': ['women', 'autumn'],
    'dress_f': ['women', 'dress'],
    'coat_f': ['women', 'coat'],
    'top_m': ['men', 'topwear'],
    'btm_m': ['men', 'bottomwear'],
    'atm_m': ['men', 'autumn'],
    'coat_m': ['men', 'coat'],
    'acc': ['accessories', 'accessory']
}




def create_color_json(color_palette):
    with open('json/color.json', 'w', encoding='utf8') as f:
        json.dump(color_palette, f, ensure_ascii=False)


def create_data(color_palette):
    i = 1
    for each in data:

        title_cutter = each['title'].find('(')

        # clean story '\n'
        cutter = each['desc'].find('*')
        unclean_story = each['desc'][:cutter]
        cleaned_story = unclean_story.replace('\n', '')

        # generate color
        colors = random.sample(color_palette, 3)
        color = ''
        for c in colors:
            color += c[0]
            color += ', '
        
        new_collection[int('210' + str(i))]={
            'title': each['title'][:title_cutter],
            'category': category[each['subgroup']][0],
            'subcat': category[each['subgroup']][1],
            'color': color[:-1],
            'story': cleaned_story,
            'note':"手工測量為正負1-2cm誤差值是正常的",
            'size': 'XS, S, M, L, XL',
            'texture': each['ori_text'][4],
            'place': each['ori_text'][5],
            'wash': '水洗',
            'main_image': each['images'][0],
            'img': each['images'][1:4],
            'price': 499,
            'stock': 30
        }
        i += 1

    with open('json/data2.json', 'w', encoding='utf8') as f:
        json.dump(new_collection, f, ensure_ascii=False)
        print(new_collection)




