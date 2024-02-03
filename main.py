from pygame import init as pginit
from pygame import display
from pygame import event as pgevent
from pygame import QUIT, KEYDOWN, K_PAGEUP, K_PAGEDOWN, K_RETURN
from pygame import font

from map_view import MapView

from pygame_textinput import TextInputVisualizer


def main() -> None:
    pginit()
    
    size = 600, 520
    screen = display.set_mode(size)
    running = True

    textinput = TextInputVisualizer()

    map_view = MapView()

    tutorial = font.Font.render(font.Font(None, 20), "Пример ввода координат(долгота, широта): 50.2121331,34.123444", 1, "black")

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
                if event.key == K_RETURN:
                    try:
                        map_view.set_coords(tuple(map(float, textinput.value.split(','))))
                    except ValueError:
                        pass
                    except TypeError:
                        pass
        
        screen.blit(map_view.image, (0,70))
        screen.blit(tutorial, (5, 5))
        screen.blit(textinput.surface, (5, 25))
        display.flip()


if __name__ == "__main__":
    main()


