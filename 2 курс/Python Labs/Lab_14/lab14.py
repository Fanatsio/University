from sqlalchemy import create_engine

import database as db

engine = create_engine('sqlite:///database.db')
print(
    """
1. Добавить дисциплину
2. Добавить кафедру
3. Добавить вид контроля
4. Показать все дисциплины
5. Показать все кафедры

0. Выход
"""
)
while True:

    req = input("\nВыбор действия: ")

    if req == "1":
        name = input("  Название: ")
        lecture = input("  Лекций: ")
        practice = input("  Практики: ")
        labs = input("  Лаб: ")
        department_id = input("  Кафедра:  ")
        toc_id = input("  Наименование вида контроля:  ")

        db.add_discipline(name, lecture, practice, labs, department_id, toc_id)

    elif req == "2":
        name = input("  Название кафедры: ")

        db.add_department(name)

    elif req == "3":
        ToC = input("  Наименование вида контроля: ")

        db.add_type_of_control(ToC)

    elif req == "4":
        disciplines = db.all_disciplines()

        if not disciplines:
            print("  Пока пусто")

        for id_discipline, data in disciplines.items():
            print(f"  {id_discipline} ")
            print(f"    Название: {data['name']}")
            print(f"    Лекций: {data['lecture']}")
            print(f"    Практики: {data['practice']}")
            print(f"    Лабораторные: {data['labs']}")
            print(f"    Кафедра: {data['department_name']}")
            print(f"    Вид контроля: {data['type_name']}")

    elif req == "5":
        departments = db.all_department()

        if not departments:
            print("  Пока пусто")

        for id_department, data in departments.items():
            print(f"  {id_department}.  ")
            print(f"  {data['name']}, Количество дисциплин: {data['count_disciplines']} ")

    elif req == "0":
        exit()

    else:
        print("Введена неверная команда")
