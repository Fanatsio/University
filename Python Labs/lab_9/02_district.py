#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Составить список всех живущих на районе (пакет district) и Вывести на консоль через запятую
# Формат вывода: На районе живут ...
# подсказка: для вывода элементов списка через запятую можно использовать функцию строки .join()
# https://docs.python.org/3/library/stdtypes.html#str.join
import district.soviet_street.house1.room1 as r1, district.soviet_street.house1.room2 as r2
import district.soviet_street.house2.room1 as r3, district.soviet_street.house2.room2 as r4
import district.central_street.house1.room1 as r5, district.central_street.house1.room2 as r6
import district.central_street.house2.room1 as r7, district.central_street.house2.room2 as r8
res = []
res += r1.folks + r2.folks + r3.folks + r4.folks + r5.folks + r6.folks + r7.folks + r8.folks
print("На районе живут:", ', '.join(res))