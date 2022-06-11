import json
import re

from bs4 import BeautifulSoup

from constants import MONOMAX_URL, YANDEX_API_KEY

import requests

from yandex_geocoder import Client


client = Client(YANDEX_API_KEY)

q = requests.get(MONOMAX_URL)
res = q.content

soup = BeautifulSoup(res, "lxml")
shop_name = soup.find("a", class_="logo").find("img")["title"]  # parse name of shop
shops = soup.find_all("div", class_="shop")

data = []
for shop in shops:
    # parse address of shop
    raw_address = shop.find("p", class_="name").text
    raw_address2 = re.sub("\(\w+ \w+\)", "", raw_address)
    shop_address = re.sub(",$", "", raw_address2).strip()

    # parse coordinates of shop
    coordinates = client.coordinates(shop_address)
    shop_latlon = [float(coordinates[1]), float(coordinates[0])]

    # parse phones of shop
    raw_phones = shop.find("p", class_="phone").find("a").text
    if "(" or ")" in raw_phones:
        raw_phones = raw_phones.replace("(", "").replace(")", "")
    shop_phones = [raw_phones.replace(" ", "")]

    # all info about shop
    shop_info = {
        "address": shop_address,
        "latlon": shop_latlon,
        "name": shop_name,
        "phones": shop_phones,
    }
    data.append(shop_info)

with open("monomax_shops_info.json", "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
