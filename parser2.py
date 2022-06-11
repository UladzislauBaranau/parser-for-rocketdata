import json
import re

from bs4 import BeautifulSoup

from constants import YANDEX_API_KEY, ZIKO_URL

import requests

from yandex_geocoder import Client


client = Client(YANDEX_API_KEY)

q = requests.get(ZIKO_URL)
res = q.content

soup = BeautifulSoup(res, "lxml")
pharmacies = soup.find(
    "tbody", class_="mp-pharmacies-table-elements clearfix"
).find_all("tr")

data = []
for pharmacy in pharmacies:
    pharmacy_address_and_phones = pharmacy.find("td", class_="mp-table-address").text

    # parse address of pharmacy
    raw_pharmacy_address = pharmacy_address_and_phones.split("tel.")
    pharmacy_address = raw_pharmacy_address[0].strip()

    # parse phones of pharmacy
    pharmacy_phones = [
        re.search("(\d{2} \d{3} \d{2} \d{2})", pharmacy_address_and_phones).group(0)
    ]

    # parse coordinates of pharmacy
    coordinates = client.coordinates(pharmacy_address)
    pharmacy_latlon = [float(coordinates[1]), float(coordinates[0])]

    # parse working_dates of pharmacy
    raw_pharmacy_working_hours = pharmacy.find("td", class_="mp-table-hours").find_all(
        "span"
    )

    l_working_hours, l_working_days = [], []
    n_iter = 0
    for working_datas in raw_pharmacy_working_hours:
        working_datas = working_datas.text.strip()
        if n_iter % 2 != 0:
            l_working_days.append(working_datas)
        else:
            l_working_hours.append(working_datas)
        n_iter += 1

    pharmacy_working_hours = list(zip(l_working_hours, l_working_days))

    # parse name of pharmacy
    pharmacy_name = pharmacy.find("span", class_="mp-pharmacy-head").text.strip()

    # all info about pharmacy
    pharmacy_info = {
        "address": pharmacy_address,
        "latlon": pharmacy_latlon,
        "name": pharmacy_name,
        "phones": pharmacy_phones,
        "working_hours": pharmacy_working_hours,
    }
    data.append(pharmacy_info)


with open("ziko_pharmacies_info.json", "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
