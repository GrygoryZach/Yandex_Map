from typing import Literal, Tuple
from pygame import sprite
from pygame import image
from requests import get
from io import BytesIO


class MapView(sprite.Sprite):
    def __init__(self, init_coords: Tuple[float, float] = (37.677751, 55.757718), init_spn: Tuple[float, float] = (0.016457,0.00619), *groups: sprite.Group) -> None:
        super().__init__(*groups)
        self.yx = init_coords
        self.spn = init_spn
        self.static_api_server = "http://static-maps.yandex.ru/1.x/"
        self.static_api_params = {
            "ll": "{0},{1}".format(*self.yx),
            "spn": "{0},{1}".format(*self.spn),
            "l": "map",
        }

        response = get(self.static_api_server, params=self.static_api_params)
        self.image = image.load(BytesIO(response.content))
        self.rect = self.image.get_rect()
    
    def move(self, direction: Literal["up", "down", "left", "right"]) -> None:
        new_y, new_x = self.yx
        match direction:
            case "up":
                new_y += 10
            case "down":
                new_y -= 10
            case "left":
                new_x -= 10
            case "right":
                new_x += 1
    
    def scale(self, scale: Literal["inc", "dec"]) -> None:
        new_spn_y, new_spn_x = self.spn
        match scale:
            case "inc":
                new_spn_x += 10
                new_spn_y += 10
            case "dec":
                new_spn_x -= 10
                new_spn_y -= 10
        self.spn = new_spn_y, new_spn_x
        self.static_api_params["spn"] = "{0},{1}".format(*self.spn)
        response = get(self.static_api_server, params=self.static_api_params)
        self.image = image.load(BytesIO(response.content))
        self.rect = self.image.get_rect()

