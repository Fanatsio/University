#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# в саду сорвали цветы
garden = ('ромашка', 'роза', 'одуванчик', 'ромашка', 'гладиолус', 'подсолнух', 'роза', )

# на лугу сорвали цветы
meadow = ('клевер', 'одуванчик', 'ромашка', 'клевер', 'мак', 'одуванчик', 'ромашка', )

# создайте множество цветов, произрастающих в саду и на лугу
# garden_set =
# meadow_set =
garden_set = set(garden)
print(garden_set)
meadow_set = set(meadow)
print(meadow_set)

print(" ")

# выведите на консоль все виды цветов
flower = garden + meadow
flower_set = set(flower)
for i in flower_set:
    print(i)

print(" ")

# выведите на консоль те, которые растут и там и там
a = garden_set & meadow_set
for i in a:
    print(i)

# выведите на консоль те, которые растут в саду, но не растут на лугу
print(garden_set.difference(meadow_set))

# выведите на консоль те, которые растут на лугу, но не растут в саду
print(meadow_set.difference(garden_set))
