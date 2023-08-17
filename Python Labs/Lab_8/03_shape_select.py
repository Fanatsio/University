# -*- coding: utf-8 -*-

import simple_draw as sd

# Запросить у пользователя желаемую фигуру посредством выбора из существующих
#   вывести список всех фигур с номерами и ждать ввода номера желаемой фигуры.
# и нарисовать эту фигуру в центре экрана

# Код функций из упр 02_global_color.py скопировать сюда
# Результат решения см results/exercise_03_shape_select.jpg

sd.resolution = (700, 700)

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

print("Выберите способ ввода:")
print("1 - Количество углов\n", "2 - Название фигуры")
choise = int(input("-> "))

if choise == 1:
    print("Введите количество углов(от 3 до 6):")
    k = int(input("-> "))
    if (k == 3):
        Triangle(sd.Point(50, 50), 60, 100, color=sd.COLOR_WHITE)
    elif (k == 4):
        Square(sd.Point(150, 150), 90, 100, color=sd.COLOR_WHITE)
    elif (k == 5):
        Pentagon(sd.Point(300, 300), 108, 99, color=sd.COLOR_WHITE)
    elif (k == 6):
        Hexagon(sd.Point(450, 450), 120, 100, color=sd.COLOR_WHITE)
    else:
        print("Вы ввели некоректный номер")
else:
    print("Выберите фигуру:")
    print("1: Треугольник\n", "2: Квадрат\n", "3: Пятиугольник\n", "4: Шестиугольник\n")
    n = int(input("-> "))
    if (n == 1):
        Triangle(sd.Point(50, 50), 59.5, 100, color=sd.COLOR_WHITE)
    elif (n == 2):
        Square(sd.Point(150, 150), 90, 100, color=sd.COLOR_WHITE)
    elif (n == 3):
        Pentagon(sd.Point(300, 300), 108, 99, color=sd.COLOR_WHITE)
    elif (n == 4):
        Hexagon(sd.Point(450, 450), 120, 100, color=sd.COLOR_WHITE)
    else:
        print("Вы ввели некоректный номер")

sd.pause()
