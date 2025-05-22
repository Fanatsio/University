import random
import time
import matplotlib.pyplot as plt
from typing import List, Callable
  
def linear_search(arr: List[int], key: int) -> int:
    """Линейный поиск: возвращает индекс ключа или -1, если ключ не найден."""
    for i, value in enumerate(arr):
        if value == key:
            return i
    return -1

def binary_search(arr: List[int], key: int) -> int:
    """Бинарный поиск: возвращает индекс ключа или -1, если ключ не найден."""
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == key:
            return mid
        right = mid - 1 if arr[mid] > key else right
        left = mid + 1 if arr[mid] < key else left
    return -1

def generate_sorted_array(size: int) -> List[int]:
    """Генерирует отсортированный массив случайных чисел."""
    return sorted(random.randint(1, 1000000) for _ in range(size))

def measure_time(search_func: Callable[[List[int], int], int], arr: List[int], key: int) -> float:
    """Измеряет время выполнения переданной функции поиска."""
    start_time = time.perf_counter()
    search_func(arr, key)
    return time.perf_counter() - start_time

def main():
    sizes = [10, 100, 1000, 10000, 100000]
    results = []

    for size in sizes:
        arr = generate_sorted_array(size)
        key = arr[len(arr) // 2]

        times = {
            'Линейный поиск': measure_time(linear_search, arr, key),
            'Двоичный поиск': measure_time(binary_search, arr, key)
        }
        results.append((size, times))

    print("Размер массива | Линейный поиск (сек) | Двоичный поиск (сек)")
    print("------------------------------------------------------------")
    for size, times in results:
        print(f"{size:13} | {times['Линейный поиск']:.8f}           | {times['Двоичный поиск']:.8f}")

    plt.figure(figsize=(10, 6))
    for label in ['Линейный поиск', 'Двоичный поиск']:
        plt.plot(
            [res[0] for res in results],
            [res[1][label] for res in results],
            marker='o', label=label
        )
    
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Размер массива (логарифмическая шкала)')
    plt.ylabel('Время выполнения (сек, логарифмическая шкала)')
    plt.title('Сравнение времени линейного и двоичного поиска')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()
