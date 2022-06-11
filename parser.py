import json

from bs4 import BeautifulSoup

from constants import YANDEX_API_KEY

from yandex_geocoder import Client


client = Client(YANDEX_API_KEY)

with open("restaurants.html") as file:
    src = file.read()

soup = BeautifulSoup(src, "lxml")
restaurants = soup.find_all("div", class_="Mujm2VkJ7g")

data = []
for restaurant in restaurants:
    # parse address of restaurant
    raw_restaurant_address = restaurant.find(
        "div", class_="_2XllDYbBnt t-m-sm mt-8"
    ).text.strip()
    l_raw_restaurant_address = raw_restaurant_address.split(",")

    restaurant_address_data = []
    for address in l_raw_restaurant_address:
        address = address.replace("\n", " ").strip()
        address = address.split()
        address = " ".join(address)
        restaurant_address_data.append(address)

    restaurant_address = ", ".join(restaurant_address_data[2:])

    # parse coordinates of restaurant
    coordinates = client.coordinates(restaurant_address)
    restaurant_latlon = [float(coordinates[1]), float(coordinates[0])]

    # parse phones of restaurant
    restaurant_phones = [
        restaurant.find("span", class_="_2p5x-cM6u6 c-primary").text.strip()
    ]

    # parse name of restaurant
    restaurant_name = restaurant.find(
        "div", class_="_3zgUWz1HVh t-xl mb-24 condensed"
    ).text.strip()

    # parse working_dates of restaurant
    raw_working_hours = restaurant.find_all("div", class_="_2I2E1lZDf7 t-m-sm mt-8")
    restaurant_working_hours = raw_working_hours[1].text.strip()

    # all info about restaurant
    restaurant_info = {
        "address": restaurant_address,
        "latlon": restaurant_latlon,
        "name": restaurant_name,
        "phones": restaurant_phones,
        "working_hours": restaurant_working_hours,
    }
    data.append(restaurant_info)


with open("kfc_restaurants_info.json", "w") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
