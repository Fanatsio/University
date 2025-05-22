import datetime
from random import randint

from double_linked_list import DoublyLinkedList, StudentNode

if __name__ == "__main__":
    students = DoublyLinkedList()

    for _ in range(10_000):
        students.append(StudentNode(
            f"Student{randint(1, 10000000)}",
            randint(1990, 2024),
            randint(2000, 2024),
            [randint(2, 5) for i in range(randint(3, 10))]
        ))

    students.append(StudentNode("ZTargetStudent", 2000, 2018, [5, 5, 5]))
    students.sort()

    time_liner_start = datetime.datetime.now()
    sf_1 = students.linear_search_by_surname("ZTargetStudent")
    print(f"Линейный поиск: {datetime.datetime.now() - time_liner_start}", sf_1)

    time_binary_start = datetime.datetime.now()
    sf_2 = students.binary_search_by_surname("ZTargetStudent")
    print(f"Бинарный поиск: {datetime.datetime.now() - time_binary_start}", sf_2)
