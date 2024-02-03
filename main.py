from pygame import init as pginit
from pygame import display
from pygame import event as pgevent
from pygame import QUIT, KEYDOWN, K_PAGEUP, K_PAGEDOWN
from pygame import sprite

from map_view import MapView


def main() -> None:
    pginit()
    
    all_sprites = sprite.Group()

    size = 600, 450
    screen = display.set_mode(size)
    running = True

    map_view = MapView()
    all_sprites.add(map_view)

    while running:
        for event in pgevent.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_PAGEUP:
                    map_view.scale("inc")
                if event.key == K_PAGEDOWN:
                    map_view.scale("dec")
        
        all_sprites.draw(screen)
        display.flip()


if __name__ == "__main__":
    main()


