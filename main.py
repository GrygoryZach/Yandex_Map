from pygame import init as pginit, sprite
from pygame import display
from pygame import event as pgevent
from pygame import QUIT, KEYDOWN, K_PAGEUP, K_PAGEDOWN, K_RETURN, MOUSEBUTTONDOWN
from pygame import font
from pygame import QUIT, KEYDOWN, K_PAGEUP, K_PAGEDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT
from pygame import sprite

from map_view import MapView, Button, coords

from pygame_textinput import TextInputVisualizer


def main() -> None:
    def set_map_veiw(map: MapView, key: str, val: str):
        map.static_api_params[key] = val
        map.do_request()

    pginit()

    size = 700, 520
    screen = display.set_mode(size)
    running = True

    textinput = TextInputVisualizer()

    button_group = sprite.Group()
    map_button = Button("data/assets/map.png", "map", (650, 100), button_group)
    sat_button = Button("data/assets/sat.png", "sat", (650, 150), button_group)
    sat_skl_button = Button("data/assets/sat_skl.png", "sat,skl", (650, 200), button_group)
    reset_button = Button("data/assets/reset.png", "reset", (620, 30), button_group)

    map_view = MapView()

    tutorial = font.Font.render(font.Font(None, 20), "Введите запрос: ", 1, "black")

    while running:
        screen.fill("white")
        events = pgevent.get()

        textinput.update(events)

        for event in events:
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
                        co = coords(textinput.value)
                        map_view.search_request(co)
                    except ValueError:
                        pass
                    except TypeError:
                        pass
            if event.type == MOUSEBUTTONDOWN:
                for i in button_group:
                    if i.rect.collidepoint(event.pos):
                        if i.label == "reset":
                            map_view.static_api_params["pt"] = ""
                            textinput.value = ""
                            map_view.do_request()
                        else:
                            i.action(set_map_veiw, map_view, "l", i.label)

        screen.blit(map_view.image, (0, 70))
        screen.blit(tutorial, (5, 5))
        screen.blit(textinput.surface, (5, 25))
        button_group.draw(screen)
        display.flip()


if __name__ == "__main__":
    main()
