from typing import Any, Literal, Tuple, Callable
from pygame import sprite
from pygame import image as pgimage
from requests import get
from io import BytesIO


class Button(sprite.Sprite):
    def __init__(self, image: str, label: str, coords: Tuple[int, int], *groups: sprite.Group) -> None:
        super().__init__(*groups)
        self.image = pgimage.load(image)
        self.rect = self.image.get_rect(center=coords)
        self.label = label

    def action(self, act: Callable, *args):
        act(*args)


class MapView(sprite.Sprite):
    def __init__(self, init_coords: Tuple[float, float] = (37.677751, 55.757718), init_zoom: int = 4,
                 *groups: sprite.Group) -> None:
        super().__init__(*groups)
        self.yx = init_coords
        self.zoom = init_zoom
        self.static_api_server = "https://static-maps.yandex.ru/1.x/"
        self.static_api_params = {
            "ll": "{0},{1}".format(*self.yx),
            "z": str(self.zoom),
            "l": "map"
        }

        self.do_request()

    def move(self, direction: Literal["up", "down", "left", "right"]) -> None:
        new_y, new_x = self.yx
        change = 360 / (2 ** self.zoom)
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

    def set_coords(self, coords: Tuple[float, float]) -> None:
        if -180 <= coords[0] <= 180 and -90 <= coords[1] <= 90:
            self.yx = coords
            self.static_api_params["ll"] = "{0},{1}".format(*self.yx)
            self.do_request()

    def do_request(self) -> None:
        response = get(self.static_api_server, params=self.static_api_params)
        self.image = pgimage.load(BytesIO(response.content))
        self.rect = self.image.get_rect()
