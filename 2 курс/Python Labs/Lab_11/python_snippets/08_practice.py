# -*- coding: utf-8 -*-

from random import randint


# Реализуем модель человека.
# Человек может есть, работать, играть, ходить в магазин.
# У человека есть степень сытости, немного еды и денег.
# Если сытость < 0 единиц, человек умирает.
# Человеку надо прожить 365 дней.
from termcolor import cprint


class Cat:
    def __init__(self):
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'сытость кота {}'.format(self.fullness)

    def eat(self):
        if self.house.catfood >= 10:
            cprint('кот поел', color='yellow')
            self.fullness += 20
            self.house.catfood -= 10
        else:
            cprint('кошачьей еды нет', color='red')

    def sleep(self):
        self.fullness -= 10
        cprint('кот спал весь день', color='yellow')

    def oboi(self):
        self.fullness -= 10
        self.house.mud += 5
        cprint('кот драл обои весь день', color='yellow')

    def act(self):
        if self.fullness <= 0:
            cprint('кот умер...', color='red')
            return
        dice = randint(1, 2)
        if self.fullness < 20 and self.house.catfood >= 10:
            self.eat()
        elif dice == 1:
            self.oboi()
        elif dice == 2:
            self.sleep()


class Man:

    def __init__(self, name):
        self.name = name
        self.fullness = 50
        self.house = None

    def __str__(self):
        return 'Я - {}, сытость {}'.format(
            self.name, self.fullness)

    def eat(self):
        if self.house.food >= 10:
            cprint('{} поел'.format(self.name), color='yellow')
            self.fullness += 10
            self.house.food -= 10
        else:
            cprint('{} нет еды'.format(self.name), color='red')

    def work(self):
        cprint('{} сходил на работу'.format(self.name), color='blue')
        self.house.money += 150
        self.fullness -= 10

    def watch_MTV(self):
        cprint('{} смотрел MTV целый день'.format(self.name), color='green')
        self.fullness -= 10

    def shopping(self):
        if self.house.money >= 50:
            cprint('{} сходил в магазин за едой'.format(self.name), color='magenta')
            self.house.money -= 50
            self.house.food += 50
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def go_to_the_house(self, house):
        self.house = house
        self.fullness -= 10
        cprint('{} Въехал в дом'.format(self.name), color='cyan')

    def buy_catfood(self):
        if self.house.money >= 50:
            self.house.money -= 50
            self.house.catfood += 50
            cprint('{} сходил в магазин за едой коту'.format(self.name), color='magenta')
        else:
            cprint('{} деньги кончились!'.format(self.name), color='red')

    def clean(self):
        self.house.mud -= 100
        self.fullness -= 20
        cprint('{} прибрался в доме'.format(self.name), color='yellow')

    def act(self):
        if self.fullness <= 0:
            cprint('{} умер...'.format(self.name), color='red')
            return
        dice = randint(1, 6)
        if self.fullness < 30 and self.house.food >= 10:
            self.eat()
        elif self.house.money < 50:
            self.work()
        elif self.house.food < 10:
            self.shopping()
        elif self.house.catfood < 10:
            self.buy_catfood()
        elif self.house.mud >= 100:
            self.clean()
        elif dice == 1:
            self.shopping()
        elif dice == 2:
            self.eat()
        elif dice == 3:
            self.buy_catfood()
        elif dice == 4:
            self.work()
        else:
            self.watch_MTV()

    def takecat(self, cat):
        cat.house = self.house




class House:

    def __init__(self):
        self.food = 50
        self.money = 0
        self.catfood = 0
        self.mud = 0

    def __str__(self):
        return 'В доме еды осталось {}, денег осталось {}, кошачьей еды осталось {}, грязи {}'.format(
            self.food, self.money, self.catfood, self.mud)


citizens = [
    Man(name='Бивис'),
    # Man(name='Батхед'),
    # Man(name='Кенни'),
]
cat = Cat()
my_sweet_home = House()
for citisen in citizens:
    citisen.go_to_the_house(house=my_sweet_home)
citizens[0].takecat(cat)

for day in range(1, 366):
    print('================ день {} =================='.format(day))
    for citisen in citizens:
        citisen.act()
    cat.act()
    print('--- в конце дня ---')
    for citisen in citizens:
        print(citisen)
    print(my_sweet_home)
    print(cat)

# Создадим двух людей, живущих в одном доме - Бивиса и Батхеда
# Нужен класс Дом, в нем должн быть холодильник с едой и тумбочка с деньгами
# Еда пусть хранится в холодильнике в доме, а деньги - в тумбочке.
