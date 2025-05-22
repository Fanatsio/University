#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import simple_draw as sd
import time

sd.resolution = (1500, 900)

# Нарисовать пузырек - три вложенных окружностей с шагом 5 пикселей
# TODO здесь ваш код
sd.clear_screen()
point = sd.get_point(100, 800)
radius = 50
for _ in range(3):
    radius += 5
    sd.circle(center_position=point, radius=radius)
#sd.circle(center_position=point)


# Написать функцию рисования пузырька, принммающую 3 (или более) параметра: точка рисования, шаг и цвет
# TODO здесь ваш код
time.sleep(1)
sd.clear_screen()
def bubble(point=sd.get_point(600, 300), step=5, color=sd.COLOR_BLUE, radius=20, *args, **kwargs):
    for _ in range(3):
        radius += step
        sd.circle(center_position=point, radius=radius, color=color)

bubble(point=point, step=10, color=sd.COLOR_RED)


# Нарисовать 10 пузырьков в ряд
# TODO здесь ваш код
time.sleep(1)
sd.clear_screen()
for x in range(100, 1100, 100):
    point = sd.get_point(x, 600)
    bubble(point=point, step=10)

# Нарисовать три ряда по 10 пузырьков
time.sleep(1)
sd.clear_screen()
for y in range(200, 500, 100):
    for x in range(100, 1100, 100):
        point = sd.get_point(x, y)
        bubble(point=point, step=10, color=sd.COLOR_ORANGE)

# Нарисовать 100 пузырьков в произвольных местах экрана случайными цветами
# TODO здесь ваш код
time.sleep(1)
sd.clear_screen()
for _ in range(100):
    point = sd.random_point()
    color = sd.random_color()
    bubble(point=point, step=5, color=color)

sd.pause()
