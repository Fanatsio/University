from typing import List, Union

class Sort:
    def __init__(self):
        self._steps: List[List[Union[int, str]]] = []

    def sort(self, data: List[Union[int, str]]) -> List[Union[int, str]]:
        raise NotImplementedError("Метод sort должен быть реализован в подклассе.")

    def _record_step(self, data: List[Union[int, str]]) -> None:
        self._steps.append(data.copy())

    def get_steps(self) -> List[List[Union[int, str]]]:
        return self._steps

class RadixSort(Sort):
    def sort(self, data: List[Union[int, str]]) -> List[Union[int, str]]:
        if not data:
            return data

        if all(isinstance(item, int) for item in data):
            return self._sort_numbers(data)
        elif all(isinstance(item, str) for item in data):
            return self._sort_strings(data)
        else:
            raise ValueError("Входной массив должен содержать только целые числа или только строки.")

    def _sort_numbers(self, data: List[int]) -> List[int]:
        max_num = max(data)
        max_length = len(str(max_num))

        for i in range(max_length):
            buckets = [[] for _ in range(10)]
            for num in data:
                digit = (num // (10 ** i)) % 10
                buckets[digit].append(num)
            data = [num for bucket in buckets for num in bucket]
            self._record_step(data)
        return data

    def _sort_strings(self, data: List[str]) -> List[str]:
        max_length = max(len(item) for item in data)

        for i in range(max_length - 1, -1, -1):
            buckets = [[] for _ in range(128)]
            for item in data:
                key = ord(item[i]) if i < len(item) else 0
                buckets[key].append(item)
            data = [item for bucket in buckets for item in bucket]
            self._record_step(data)
        return data

class SelectionSort(Sort):
    def sort(self, data: List[Union[int, str]]) -> List[Union[int, str]]:
        for i in range(len(data) - 1):
            min_index = i
            for j in range(i + 1, len(data)):
                if data[j] < data[min_index]:
                    min_index = j
            data[i], data[min_index] = data[min_index], data[i]
            self._record_step(data)
        return data

class SortWithSteps:
    def __init__(self, sort_algorithm: Sort):
        self.sort_algorithm = sort_algorithm

    def sort(self, data: List[Union[int, str]]) -> List[Union[int, str]]:
        return self.sort_algorithm.sort(data)

    def visualize_sorting(self) -> None:
        steps = self.sort_algorithm.get_steps()
        for i, step in enumerate(steps, start=1):
            print(f"Шаг {i}: {', '.join(map(str, step))}")
            print("-" * 20)

def menu() -> int:
    while True:
        try:
            choice = int(input("1 - Сортировка выбором\n"
                               "2 - Поразрядная сортировка\n"
                               "3 - Сменить набор данных\n"
                               "0 - Выход\n"
                               "Введите >> "))
            if choice in [0, 1, 2, 3]:
                return choice
            else:
                print("Неверный выбор. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

data_1 = [5, 6, 10, 1, 15, 4]
data_2 = ["michelle", "tigger", "sunshine", "chocolate", "password1", "soccer", "anthony"]

current_data = data_1

print(f"Массив до сортировки: {current_data}")

selection_sort = SortWithSteps(SelectionSort())
radix_sort = SortWithSteps(RadixSort())

while True:
    choice = menu()
    if choice == 0:
        print("Выход из программы.")
        break
    elif choice == 1:
        sorted_data = selection_sort.sort(current_data.copy())
        selection_sort.visualize_sorting()
        print(f"Результат сортировки выбором: {sorted_data}")
    elif choice == 2:
        sorted_data = radix_sort.sort(current_data.copy())
        radix_sort.visualize_sorting()
        print(f"Результат поразрядной сортировки: {sorted_data}")
    elif choice == 3:
        current_data = data_2 if current_data == data_1 else data_1
        print(f"Текущий массив для сортировки: {current_data}")
