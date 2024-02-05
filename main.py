import sys
from io import BytesIO
# Этот класс поможет нам сделать картинку из потока байт

import requests
from PIL import Image

from distance import lonlat_distance

# address_ll = sys.argv[1]
address_ll = "37.588392,55.734036"

search_api_server = "https://search-maps.yandex.ru/v1/"
api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"

search_params = {
    "apikey": api_key,
    "text": "аптека",
    "lang": "ru_RU",
    "ll": address_ll,
    "type": "biz"
}

response = requests.get(search_api_server, params=search_params)
if not response:
    # ...
    pass

# Преобразуем ответ в json-объект
json_response = response.json()

points = []
delta = -10 ** 9
for i in range(10):
    organization = json_response["features"][i]
    point = organization["geometry"]["coordinates"]
    org_point = "{0},{1}".format(point[0], point[1])
    points.append(f'{org_point},pm2dgl')
    x = list(map(float, address_ll.split(',')))
    y = list(map(float, org_point.split(',')))

    delta = max(abs(x[0] - y[0]), abs(x[1] - y[1]), delta)


delta = str(delta)


# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    # позиционируем карту центром на наш исходный адрес
    "ll": address_ll,
    "spn": ",".join([delta, delta]),
    "l": "map",
    # добавим точку, чтобы указать найденную аптеку
    "pt": "~".join(points)
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()

# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
