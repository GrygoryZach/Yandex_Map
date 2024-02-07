from cProfile import label
from typing import Tuple
from pygame import init as pginit, sprite
from pygame import display
from pygame import event as pgevent
from pygame import (QUIT, KEYDOWN, K_PAGEUP, K_PAGEDOWN, K_RETURN, 
                    MOUSEBUTTONDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT,
                    K_BACKSPACE, MOUSEBUTTONUP
                    )
from pygame import font
from pygame import sprite
from pygame import Color
from pygame import Rect
from pygame import draw
from pygame import Surface

from map_view import MapView, Button, coords

pginit()

COLOR_INACTIVE = Color('lightskyblue3')
COLOR_ACTIVE = Color('dodgerblue2')
FONT = font.Font(None, 32)


class Switcher:
    def __init__(self, coords: Tuple[int, int]) -> None:
        self.item = Surface((40, 40))
        self.rect = self.item.get_rect(topleft=coords)
        self.clicked = False
        self.color = False
        self.coords = coords
        self.n = 0
        self.label = ""
        self.label2 = ""

    def handle_event(self, event: pgevent.Event):
        if event.type == MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            if not self.clicked:
                self.color = not self.color
                self.clicked = True
                self.n = not self.n
        if event.type == MOUSEBUTTONUP:
            self.clicked = False

    def draw(self, screen: Surface) -> None:
        if self.color:
            self.item.fill((0, 255, 0))
        else:
            self.item.fill((255, 0, 0))
        screen.blit(self.item, self.coords)


class InputBox:
    def __init__(self, x: int, y: int, w: int, h: int, text=''):
        self.rect = Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event: pgevent.Event):
        if event.type == MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == KEYDOWN:
            if self.active:
                if event.key == K_RETURN:
                    print(self.text)
                elif event.key == K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen: Surface):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        draw.rect(screen, self.color, self.rect, 2)


def main() -> None:
    def set_map_veiw(map: MapView, key: str, val: str):
        map.static_api_params[key] = val
        map.do_request()

    size = 700, 560
    screen = display.set_mode(size)
    running = True

    address_box = InputBox(10, 30, 400, 30)
    # postcode_box = InputBox(20, 522, 400, 30)

    button_group = sprite.Group()
    map_button = Button("data/assets/map.png", "map", (650, 100), button_group)
    sat_button = Button("data/assets/sat.png", "sat", (650, 150), button_group)
    sat_skl_button = Button("data/assets/sat_skl.png", "sat,skl", (650, 200), button_group)
    reset_button = Button("data/assets/reset.png", "reset", (620, 30), button_group)
    
    switcher = Switcher((600, 500))

    map_view = MapView((0, 70))

    tutorial = font.Font.render(font.Font(None, 20), "Введите запрос:", False, "black")
    postcode = ""

    while running:
        screen.fill("white")
        events = pgevent.get()


        for event in events:
            # postcode_box.handle_event(event)
            address_box.handle_event(event)
            switcher.handle_event(event)
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_PAGEUP:
                    map_view.scale("inc")
                if event.key == K_PAGEDOWN:
                    map_view.scale("dec")
                if event.key == K_UP:
                    map_view.move("up")
                if event.key == K_DOWN:
                    map_view.move("down")
                if event.key == K_LEFT:
                    map_view.move("left")
                if event.key == K_RIGHT:
                    map_view.move("right")
                if event.key == K_RETURN:
                    try:
                        address = address_box.text
                        cor_req = coords(address.strip())
                        co = cor_req[0]
                        map_view.search_request(co)
                        tutorial = font.Font.render(font.Font(None, 20), cor_req[1], False, "black")
                        postcode = cor_req[2]
                    except ValueError:
                        pass
                    except TypeError:
                        pass
            if event.type == MOUSEBUTTONDOWN:
                if map_view.rect.collidepoint(event.pos):
                    cor_req = map_view.set_point(*event.pos)
                    tutorial = font.Font.render(font.Font(None, 20), cor_req[1], False, "black")
                    postcode = cor_req[2]
                for i in button_group:
                    if i.rect.collidepoint(event.pos):
                        if i.label == "reset":
                            map_view.static_api_params["pt"] = ""
                            address_box.text = ""
                            address_box.txt_surface = FONT.render("", True, address_box.color)
                            postcode = ""
                            map_view.do_request()
                            tutorial = font.Font.render(font.Font(None, 20), "Введите запрос:", False, "black")
                        else:
                            i.action(set_map_veiw, map_view, "l", i.label)

        screen.blit(map_view.image, map_view.rect)
        screen.blit(tutorial, (5, 5))
        button_group.draw(screen)
        address_box.draw(screen)
        if switcher.n:
            screen.blit(font.Font.render(font.Font(None, 20), postcode, False, "black"), (400, 520))
        switcher.draw(screen)
        screen.blit(font.Font.render(font.Font(None, 20), "postcode", False, "black"), (600, 480))
        display.flip()


if __name__ == "__main__":
    main()
