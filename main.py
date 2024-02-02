import os
import sys

import pygame
import requests

coords = "28.97709,41.005233" # input("Введите координаты через запятую (к примеру 134.13,-24.47): ")
scale = "4" # input("Введите уровень масштабирования карты от 0 до 21: ")
map_request = "https://static-maps.yandex.ru/1.x/"
map_params = {
    "ll": "134.13992626725712,-24.478902738123082",
    "spn": "50,50",
    "lang": "ru_RU",
    "l": "sat",
}
response = requests.get(map_request, params=map_params)

if not response:
    print("Ошибка выполнения запроса:")
    print(response.url)
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
