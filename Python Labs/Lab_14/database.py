from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import models

engine = create_engine('sqlite:///database.db')
session = Session(bind=engine)

def add_type_of_control(name):
    name_toc = session.query(models.Type_of_control).filter(models.Type_of_control.name == name)

    if name_toc.count() != 0:
        return print("Данный вид контроля уже есть в базе данных")

    new_type = models.Type_of_control(
        name=name
    )

    session.add(new_type)
    session.commit()


def add_department(name):
    department = session.query(models.department).filter(models.department.name == name)

    if department.count() != 0:
        return print("Данная кафедра уже есть")

    new_department = models.department(
        name=name
    )
    session.add(new_department)
    session.commit()


def add_discipline(name, lecture, practice, labs, department_id, toc_id):
    departments = session.query(models.department).filter(models.department.id == department_id)

    types = session.query(models.Type_of_control).filter(models.Type_of_control.id == toc_id)


    new_discipline = models.Discipline(
        name=name,
        lecture=lecture,
        practice=practice,
        labs=labs,
        department_id=department_id,
        type_of_control_id=toc_id
    )
    if departments.count() == 0:
        return print(f'Номер кафедры {department_id} не найден')
    elif types.count() == 0:
        return print(f"Данный вид контроля:{toc_id} не найден")

    session.add(new_discipline)
    session.commit()

def all_disciplines():
    result = {}

    disciplines = session.query(models.Discipline).all()

    for discipline in disciplines:
        result[str(discipline.id)] = {
            "name": discipline.name,
            "lecture": discipline.lecture,
            "practice": discipline.practice,
            "labs": discipline.labs
        }
        departments = session.query(models.department).filter(models.department.id == discipline.department_id)
        for p in departments:
            result[str(discipline.id)].update({
                "department_name": p.name
            })
        types = session.query(models.Type_of_control).filter(
            models.Type_of_control.id == discipline.type_of_control_id)
        for t in types:
            result[str(discipline.id)].update({
                "type_name": t.name
            })
    return result


def all_department():
    result = {}
    departments = session.query(models.department).all()

    count = 0
    disciplines = session.query(models.Discipline).all()

    for department in departments:
        for discipline in disciplines:
            if discipline.department_id == department.id:
                count += 1

        result[str(department.id)] = {
            "name": department.name,
            "count_disciplines": count
        }
        count = 0

    return result

    # def all_types_of_control():
    #     types = session.query(models.Type_of_control).all()
    #
    #     return {str(i.id): i.title for i in types}
