from typing import Any, Literal, Tuple, Callable
from pygame import sprite
from pygame import image as pgimage
from requests import get
from io import BytesIO
from math import cos, radians


class Button(sprite.Sprite):
    def __init__(self, image: str, label: str, cords: Tuple[int, int], *groups: sprite.Group) -> None:
        super().__init__(*groups)
        self.image = pgimage.load(image)
        self.rect = self.image.get_rect(center=cords)
        self.label = label

    def action(self, act: Callable, *args):
        act(*args)


def coords(name: str):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/"
    params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": name,
        "format": "json"
    }
    response = get(geocoder_request, params=params)
    if response:
        json_response = response.json()
        ans = json_response["response"]["GeoObjectCollection"]["featureMember"][0][
            "GeoObject"]["Point"]["pos"]
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        print(response.url)
        try:
            post_index = toponym["metaDataProperty"]["GeocoderMetaData"]['Address']['postal_code']
        except:
            post_index = ''
        return (tuple(map(float, ans.split())), f"{toponym_address}", post_index)
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


class MapView(sprite.Sprite):
    def __init__(self, window_loc: Tuple[int, int], init_coords: Tuple[float, float] = (37.677751, 55.757718), init_zoom: int = 4,
                 *groups: sprite.Group) -> None:
        super().__init__(*groups)
        self.yx = init_coords
        self.zoom = init_zoom
        self.static_api_server = "https://static-maps.yandex.ru/1.x/"
        self.static_api_params = {
            "ll": "{0},{1}".format(*self.yx),
            "z": str(self.zoom),
            "l": "map",
            "pt": ""
        }
        self.window_loc = window_loc

        self.current_postcode = ""

        self.do_request()

    def move(self, direction: Literal["up", "down", "left", "right"]) -> None:
        new_y, new_x = self.yx
        change = 200 / (2 ** self.zoom)
        match direction:
            case "up":
                if new_x + change < 100:
                    new_x += change
            case "down":
                if new_x - change > -100:
                    new_x -= change
            case "left":
                new_y -= change
            case "right":
                new_y += change

        self.yx = new_y, new_x
        self.static_api_params["ll"] = "{0},{1}".format(*self.yx)
        self.do_request()

    def scale(self, scale: Literal["inc", "dec"]) -> None:
        match scale:
            case "inc":
                if 0 <= self.zoom + 1 <= 21:
                    self.zoom += 1
            case "dec":
                if 0 <= self.zoom - 1 <= 21:
                    self.zoom -= 1
        self.static_api_params["z"] = str(self.zoom)
        self.do_request()

    def search_request(self, crds: Tuple[float, float]) -> None:
        if crds:
            self.yx = crds
            self.static_api_params["ll"] = "{0},{1}".format(*self.yx)
            self.static_api_params["pt"] = "{0},{1}".format(*self.yx)
            self.do_request()

    def do_request(self) -> None:
        response = get(self.static_api_server, params=self.static_api_params)
        self.image = pgimage.load(BytesIO(response.content))
        self.rect = self.image.get_rect(topleft=self.window_loc)

    def set_point(self, x: int, y: int):
        dx = x - 300
        dy = 255 - y + 35
        curr_lon, curr_lat = map(float, self.static_api_params["ll"].split(','))
        # coord_to_geo_x, coord_to_geo_y = 0.0000428, 0.0000428
        new_lon = curr_lon + dx * 360 / (2 ** (8 + self.zoom)) # * coord_to_geo_x * 2 ** (15 - self.zoom)
        new_lat = curr_lat + dy * 180 / (2 ** (8 + self.zoom)) # * coord_to_geo_y * cos(radians(curr_lat)) * 2 ** (15 - self.zoom)
        self.static_api_params["ll"] = "{0},{1}".format(new_lon, new_lat)
        self.static_api_params["pt"] = "{0},{1}".format(new_lon, new_lat)
        self.do_request()
        return coords(self.static_api_params["ll"])
    
    def found_organization(self):
        search_api_service = "https://search-maps.yandex.ru/v1/"
        search_api_params = {
            "apikey": "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3",
            "text": ','.join(self.static_api_params["ll"].split(',')[::-1]),
            "lang": "ru-RU",
            "type": "biz"
        }
        response = get(search_api_service, params=search_api_params)
        if response:
            print(response.url)
            json_resp = response.json()
            obj_geometry = json_resp["features"][0]["geometry"]["coordinates"]
            lon, lat = obj_geometry
            curr_lat, curr_lon = map(float, self.static_api_params["ll"].split(','))
            dx = (lon - curr_lon) * 111
            dy = (lat - curr_lat) * 111
            if (dx ** 2 + dy ** 2) ** 0.5 <= 50:
                obj = json_resp["features"][0]["properties"]
                return obj["name"] + ', ' + obj["description"]

            return None

