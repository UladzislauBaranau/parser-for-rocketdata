## Python scripts to extract the necessary information
Scripts help quickly collect data about addresses, names, phones, operating modes, and coordinates.

### Installation and Running

#### Development tools
Creating and activating virtual environment:
```
python3 -m venv .venv
. ./.venv/bin/activate
```
Installing dependencies:
```
pip install -r requirements.txt
```

#### Yandex geocoder
To correctly do Yandex geocoder work, you need to replace [this key](https://github.com/UladzislauBaranau/parser-for-rocketdata/blob/master/constants.py#L1) with a personal one. If you don't have an API key,  you can get it [this](https://yandex.ru/dev/maps/geocoder/).

#### Running
You can run them alternately, or you can run them simultaneously:
```
python3 parser.py
python3 parser2.py
python3 parser3.py
```

### Expected result
The required information is stored in **JSON** files, there are *kfc_restaurants_info*, *ziko_pharmacies_info*, and *monomax_shops_info*.
<br>
<br> *kfc_restaurants_info.json* example:
```
[
  ...
  {
        "address": "Москва, Малая Юшуньская, 1к1",
        "latlon": [
            55.653223,
            37.594513
        ],
        "name": "KFC Берлин Москва",
        "phones": [
            "+74953198531"
        ],
        "working_hours": "Пн-Пт: 10:00 — 22:00"
    },
    ...
]
```
*ziko_pharmacies_info.json* example:
```
[
  ...
    {
        "address": "ul. Norberta Barlickiego 7 (w biurowcu OSCAR) Bielsko-Biała",
        "latlon": [
            49.823263,
            19.045721
        ],
        "name": "Ziko Dermo",
        "phones": [
            "33 484 81 50"
        ],
        "working_hours": [
            [
                "pon-pt",
                "08:00 - 20:00"
            ],
            [
                "sobota",
                "08:00 - 15:00"
            ]
        ]
    },
  ...
]
```
*monomax_shops_info.json* example:
```
[
  ...
    {
        "address": "ул. Кропоткина, 72",
        "latlon": [
            53.918386,
            27.557789
        ],
        "name": "Мономах",
        "phones": [
            "+375173342686"
        ]
    },
 ...
]
```
