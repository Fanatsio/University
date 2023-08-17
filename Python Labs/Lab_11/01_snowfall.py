# -*- coding: utf-8 -*-

import simple_draw as sd
sd.resolution = (1200, 600)
# Шаг 1: Реализовать падение снежинки через класс. Внести в методы:
#  - создание снежинки с нужными параметрами
#  - отработку изменений координат
#  - отрисовку


class Snowflake:
    def __init__(self):
        self.len = sd.random_number(10, 50)
        self.coords = sd.get_point(sd.random_number(200, 1000), sd.random_number(550, 900))
    def move(self):
        self.coords.x += sd.random_number(-10, 10)
        self.coords.y -= 10
    def draw(self):
        sd.snowflake(length=self.len, center=self.coords)
    def can_fall(self):
        return self.coords.y > self.len
    def clear_previous_picture(self):
        sd.snowflake(length=self.len, center=self.coords, color=sd.background_color)


flake = Snowflake()

N = 20


# шаг 2: создать снегопад - список объектов Снежинка в отдельном списке, обработку примерно так:
  # создать список снежинок

def get_flakes(count):
    return [Snowflake() for _ in range(count)]

flakes = get_flakes(count=N)

def get_fallen_flakes():
    global flakes
    res = 0
    for flake in flakes:
        if not flake.can_fall():
            res += 1
            flakes.remove(flake)
    return res
def append_flakes(count):
    global flakes
    for _ in range(count):
        flake = Snowflake()
        flakes.append(flake)
while True:
    for flake in flakes:
        flake.clear_previous_picture()
        flake.move()
        flake.draw()
    fallen_flakes = get_fallen_flakes()
    if fallen_flakes:
        append_flakes(count=fallen_flakes)
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()
