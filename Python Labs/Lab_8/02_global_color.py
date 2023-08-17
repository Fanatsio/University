# -*- coding: utf-8 -*-
import simple_draw as sd

# Добавить цвет в функции рисования геом. фигур. из упр 01_shapes.py
# (код функций скопировать сюда и изменить)
# Запросить у пользователя цвет фигуры посредством выбора из существующих:
#   вывести список всех цветов с номерами и ждать ввода номера желаемого цвета.
# Потом нарисовать все фигуры этим цветом

# Пригодятся функции
# sd.get_point()
# sd.line()
# sd.get_vector()
# и константы COLOR_RED, COLOR_ORANGE, COLOR_YELLOW, COLOR_GREEN, COLOR_CYAN, COLOR_BLUE, COLOR_PURPLE
# Результат решения см /results/exercise_02_global_color.jpg

sd.resolution = (700, 700)

Color_dictionary = {
    1: sd.COLOR_BLUE,
    2: sd.COLOR_GREEN,
    3: sd.COLOR_RED,
    4: sd.COLOR_ORANGE,
    5: sd.COLOR_YELLOW,
    6: sd.COLOR_CYAN,
    7: sd.COLOR_PURPLE 
}

def Figure(Point, angle, len, angle_dif, color, n):
    for _ in range(n):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=color, width=2)
        sd.line(Point, end_point, color=color, width=3)
        angle -= angle_dif
        Point = end_point

def Triangle(Point, angle, len, color):
    angle_dif = 120
    Figure(Point, angle, len, angle_dif, color, 3)

def Square(Point, angle, len, color):
    angle_dif = 90
    Figure(Point, angle, len, angle_dif, color, 4)

def Pentagon(Point, angle, len, color):
    angle_dif = 72
    Figure(Point, angle, len, angle_dif, color, 5)

def Hexagon(Point, angle, len, color):
    angle_dif = 60
    Figure(Point, angle, len, angle_dif, color, 6)

print("Выберите цвет:")
print("1: Синий\n", "2: Зеленый\n", "3: Красный\n", "4: Оранжевый\n", "5: Желтый\n", "6: Голубой\n", "7: Розовый\n")
n = int(input("-> "))

if (n <= 7):
    color = Color_dictionary[n]
    Triangle(sd.Point(50, 50), 59.5, 100, color)
    Square(sd.Point(150, 150), 90, 100, color)
    Pentagon(sd.Point(300, 300), 108, 99, color)
    Hexagon(sd.Point(450, 450), 120, 100, color)
else:
    print("Вы ввели некоректный номер")

sd.pause()
