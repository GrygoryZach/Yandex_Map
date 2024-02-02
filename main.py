import os
import sys

import pygame
import requests

coords = input("Введите координаты через запятую (к примеру 134.13,-24.47): ")
scale = input("Введите уровень масштабирования карты от 0 до 21: ")
map_request = f"https://static-maps.yandex.ru/1.x/?ll={coords}&z={scale}&l=sat"
response = requests.get(map_request)

if not response:
    print("Ошибка выполнения запроса:")
    print(map_request)
    print("Http статус:", response.status_code, "(", response.reason, ")")
    sys.exit(1)

map_file = "map.png"
with open(map_file, "wb") as file:
    file.write(response.content)

pygame.init()
screen = pygame.display.set_mode((600, 450))
screen.blit(pygame.image.load(map_file), (0, 0))
pygame.display.flip()
while pygame.event.wait().type != pygame.QUIT:
    pass
pygame.quit()

os.remove(map_file)
