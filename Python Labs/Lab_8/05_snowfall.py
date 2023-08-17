# -*- coding: utf-8 -*-

import simple_draw as sd
width = 1200
height = 800
sd.resolution = (width, height)

# На основе кода из практической части реализовать снегопад:
# - создать списки данных для отрисовки N снежинок
# - нарисовать падение этих N снежинок
# - создать список рандомных длинн лучей снежинок (от 10 до 100) и пусть все снежинки будут разные

N = 20

# Пригодятся функции
# sd.get_point()
# sd.snowflake()
# sd.sleep()
# sd.random_number()
# sd.user_want_exit()

def snowflake_gen():
    return {'length': sd.random_number(8, 24),
            'x': sd.randint(10, width - 10),
            'y': height + sd.randint(100, 150),
            'factor_a': sd.random_number(4, 7) / 10,
            'factor_b': sd.random_number(4, 7) / 10,
            'factor_c': sd.random_number(45, 60)
            }

snowflakes = []
for _ in range(N):
    snowflakes.append(snowflake_gen())
i = 0
sd.start_drawing()
while True:
    for snowflake in snowflakes:
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            point, snowflake['length'],
            sd.background_color,
            snowflake['factor_a'],
            snowflake['factor_b'],
            snowflake['factor_c'])
        snowflake['x'] -= sd.randint(-10, 10)
        snowflake['y'] -= sd.randint(10, 25)
        point = sd.get_point(snowflake['x'], snowflake['y'])
        sd.snowflake(
            point, snowflake['length'],
            sd.COLOR_WHITE,
            snowflake['factor_a'],
            snowflake['factor_b'],
            snowflake['factor_c'])
        if snowflake['y'] < sd.randint(0, 40):
            snowflakes.remove(snowflake)
    i += 1
    if i % 2 == 0:
        new_snowflake = snowflake_gen()
        snowflakes.append(snowflake_gen())
    sd.finish_drawing()
    sd.sleep(0.1)
    if sd.user_want_exit():
        break

sd.pause()

# Примерный алгоритм отрисовки снежинок
#   навсегда
#     очистка экрана
#     для индекс, координата_х из списка координат снежинок
#       получить координата_у по индексу
#       создать точку отрисовки снежинки
#       нарисовать снежинку цветом фона
#       изменить координата_у и запомнить её в списке по индексу
#       создать новую точку отрисовки снежинки
#       нарисовать снежинку на новом месте белым цветом
#     немного поспать
#     если пользователь хочет выйти
#       прервать цикл


# Часть 2 (делается после зачета первой части)
#
# Ускорить отрисовку снегопада
# - убрать clear_screen() из цикла
# - в начале рисования всех снежинок вызвать sd.start_drawing()
# - на старом месте снежинки отрисовать её же, но цветом sd.background_color
# - сдвинуть снежинку
# - отрисовать её цветом sd.COLOR_WHITE на новом месте
# - после отрисовки всех снежинок, перед sleep(), вызвать sd.finish_drawing()

# Усложненное задание (делать по желанию)
# - сделать рандомные отклонения вправо/влево при каждом шаге
# - сделать сугоб внизу экрана - если снежинка долетает до низа, оставлять её там,
#   и добавлять новую снежинку
# Результат решения см https://youtu.be/XBx0JtxHiLg

