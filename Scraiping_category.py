import requests
import re
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
from pymongo import MongoClient

client = MongoClient("localhost", 27017)
db = client.category
collection = db.category_collection
collection.delete_many({})

all_list=[]

def first(target_url):
    r = requests.get(target_url)
    bs = BeautifulSoup(r.text, "lxml")
    return bs

def second(Soup):
    pass_name = []
    pass_url = []
    for b in Soup.find_all("ul",class_="sub_categories"):
        for b1 in b.find_all("a"):
            href1 = b1.get("href")
            path1 = urljoin(cookpad_url, href1)
            ex1 = b1.text
            pass_name.append(ex1)
            pass_url.append(path1)
            
    return pass_name,pass_url
    

def third(bSoup):
    recipe_name = []
    recipe_url = []
    for be in bSoup.find_all("div", class_="recipe-text"):
        bee = be.find("a")
        href2 = bee.get("href")
        path2 = urljoin(cookpad_url, href2)
        ex2 = bee.text
        recipe_name.append(ex2)
        recipe_url.append(path2)
    return recipe_name,recipe_url

def fourth(i1):
    count=first(i1).find("span" ,class_="search_count")
    repatter = re.compile(',')
    tx = re.sub(repatter, '', count.text)
    rrepatter = re.compile('\n')
    txt = re.sub(rrepatter, '',tx)
    return txt

def fifth():
    jufuku = collection.find_one({"path" : URL})
    if not jufuku:
        collection.insert_one({
            "level" : n,
            "oya_category" : matchObject.group(),
            "category_name" : 名前,
            "recipe_count" : cou,
            "category_number" : maObject.group(),
            "path" : URL,
        })
        
#level_1
cookpad_url = "https://cookpad.com/category/list"
bs_cookpad = first(cookpad_url)

regex = r'/category/\d'
level_1_url_list = []
for a in bs_cookpad.find_all("div", class_="root_category_title_wrapper"):
    ex = a.find("a").text
    for a1 in a.find_all(href=re.compile(regex)):
        href = a1.get("href")
        path = urljoin(cookpad_url, href)
        cou = fourth(path)
        matchObject = re.search(r'[\d]+',path)
        level_1_url_list.append(path)
        collection.insert_one({
            "level" : "1",
            "oya_category" : "-1",
            "category_name" : ex,
            "recipe_count" : cou,
            "category_number" : matchObject.group(),
            "path" : path,
        })
        print("1", "-1",ex, cou, matchObject.group(), path)
        time.sleep(1)
        
#level_2
n = 2
while n<6:
    n = str(n)
    URL_list = "URL_list"+n
    URL_list=[]
    for List in level_1_url_list:
        x,y = second(first(List))
        for (名前,URL) in zip(x,y):
            if bool(first(URL).find("span", class_="current_leaf_category")) is True:
                all_list.append(URL)
                
                matchObject = re.search(r'[\d]+', List)
                cou = fourth(URL)
                maObject = re.search(r'[\d]+',URL)
                
                fifth()
                print("✫"+n, matchObject.group(), 名前, cou, maObject.group(), URL)
                time.sleep(1)
            else:
                URL_list.append(URL)
                
                matchObject = re.search(r'[\d]+', List)
                cou = fourth(URL)
                maObject = re.search(r'[\d]+',URL)
                
                fifth()
                print(n, matchObject.group(), 名前, cou, maObject.group(), URL)
                time.sleep(1)
    level_1_url_list = URL_list
    n = int(n)
    n = n+1
print("END")