# -*- coding: utf-8 -*-

import simple_draw as sd

sd.resolution = (700, 700)

# Часть 1.
# Написать функции рисования равносторонних геометрических фигур:
# - треугольника
# - квадрата
# - пятиугольника
# - шестиугольника
# Все функции должны принимать 3 параметра:
# - точка начала рисования
# - угол наклона
# - длина стороны
#
# Примерный алгоритм внутри функции:
#   # будем рисовать с помощью векторов, каждый следующий - из конечной точки предыдущего
#   текущая_точка = начальная точка
#   для угол_наклона из диапазона от 0 до 360 с шагом XXX
#      # XXX подбирается индивидуально для каждой фигуры
#      составляем вектор из текущая_точка заданной длины с наклоном в угол_наклона
#      рисуем вектор
#      текущая_точка = конечной точке вектора
#
# Использование копи-пасты - обязательно! Даже тем кто уже знает про её пагубность. Для тренировки.
# Как работает копипаста:
#   - одну функцию написали,
#   - копипастим её, меняем название, чуть подправляем код,
#   - копипастим её, меняем название, чуть подправляем код,
#   - и так далее.
# В итоге должен получиться ПОЧТИ одинаковый код в каждой функции

# Пригодятся функции
# sd.get_point()
# sd.get_vector()
# sd.line()
# Результат решения см results/exercise_01_shapes.jpg

# TODO здесь ваш код
'''def Triangle(x, y, angle, len):
    Point = sd.Point(x, y)
    for _ in range(3):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=sd.COLOR_ORANGE, width=2)
        sd.line(Point, end_point, color=sd.COLOR_ORANGE, width=2)
        angle -= 120
        Point = end_point

def Square(x, y, angle, len):
    Point = sd.Point(x, y)
    for _ in range(4):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=sd.COLOR_ORANGE, width=2)
        sd.line(Point, end_point, color=sd.COLOR_ORANGE, width=2)
        angle -= 90
        Point = end_point

def Pentagon(x, y, angle, len):
    Point = sd.Point(x, y)
    for _ in range(5):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=sd.COLOR_ORANGE, width=2)
        sd.line(Point, end_point, color=sd.COLOR_ORANGE, width=2)
        angle -= 72
        Point = end_point

def Hexagon(x, y, angle, len):
    Point = sd.Point(x, y)
    for _ in range(6):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=sd.COLOR_ORANGE, width=2)
        sd.line(Point, end_point, color=sd.COLOR_ORANGE, width=2)
        angle -= 60
        Point = end_point'''

#Triangle(50, 50, 60, 100)
#Square(150, 150, 90, 100)
#Pentagon(300, 300, 108, 100)
#Hexagon(450, 450, 120, 100)

# Часть 1-бис.
# Попробуйте прикинуть обьем работы, если нужно будет внести изменения в этот код.
# Скажем, связывать точки не линиями, а дугами. Или двойными линиями. Или рисовать круги в угловых точках. Или...
# А если таких функций не 4, а 44? Код писать не нужно, просто представь объем работы... и запомни это.

# Часть 2 (делается после зачета первой части)
#
# Надо сформировать функцию, параметризированную в местах где была "небольшая правка".
# Это называется "Выделить общую часть алгоритма в отдельную функцию"
# Потом надо изменить функции рисования конкретных фигур - вызывать общую функцию вместо "почти" одинакового кода.
#
# В итоге должно получиться:
#   - одна общая функция со множеством параметров,
#   - все функции отрисовки треугольника/квадрата/етс берут 3 параметра и внутри себя ВЫЗЫВАЮТ общую функцию.
#
# Не забудте в этой общей функции придумать, как устранить разрыв в начальной/конечной точках рисуемой фигуры
# (если он есть. подсказка - на последней итерации можно использовать линию от первой точки)

def Figure(Point, angle, len, angle_dif, n):
    for _ in range(n):
        end_point = sd.vector(start=Point, angle=angle, length=len,color=sd.COLOR_ORANGE, width=3)
        sd.line(Point, end_point, color=sd.COLOR_ORANGE, width=3)
        angle -= angle_dif
        Point = end_point

def Triangle(Point, angle, len):
    angle_dif = 120
    Figure(Point, angle, len, angle_dif, 3)

def Square(Point, angle, len):
    angle_dif = 90
    Figure(Point, angle, len, angle_dif, 4)

def Pentagon(Point, angle, len):
    angle_dif = 72
    Figure(Point, angle, len, angle_dif, 5)

def Hexagon(Point, angle, len):
    angle_dif = 60
    Figure(Point, angle, len, angle_dif, 6)
    
Triangle(sd.Point(50, 50), 59.5, 100)
Square(sd.Point(150, 150), 90, 100)
Pentagon(sd.Point(300, 300), 108, 99)
Hexagon(sd.Point(450, 450), 120, 100)


# Часть 2-бис.
# А теперь - сколько надо работы что бы внести изменения в код? Выгода на лицо :)
# Поэтому среди программистов есть принцип D.R.Y. https://clck.ru/GEsA9
# Будьте ленивыми, не используйте копи-пасту!


sd.pause()
