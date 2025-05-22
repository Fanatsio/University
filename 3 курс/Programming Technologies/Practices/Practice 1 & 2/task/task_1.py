from copy import copy

from double_linked_list import DoublyLinkedList, StudentNode

if __name__ == "__main__":
    students = DoublyLinkedList()
    students.append(StudentNode("Речук", 2000, 2021, [1, 1, 3, 4, 5]))
    students.append(StudentNode("Иванов", 2001, 2020, [5, 2, 3, 4, 5]))
    students.append(StudentNode("Петров", 2002, 2021, [1, 3, 3, 2, 5]))
    students.append(StudentNode("Александров", 2002, 2020, [1, 3, 3, 2, 5]))
    students.append(StudentNode("Сергеев", 2002, 2021, [1, 3, 3, 2, 5]))
    students.append(StudentNode("Максимов", 2002, 2021, [1, 3, 3, 2, 5]))

    students_filtered = DoublyLinkedList()

    for student in students:
        if student.enrollment_year % 2:
            students_filtered.append(copy(student))
            students.remove(student)

    print(students)
    print(students_filtered)
