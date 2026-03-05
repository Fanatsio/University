import numpy as np
from functions import f1, f2
from numerical import coordinate_descent
from localization import localization_phase
from visualization import visualize_results

def main():
    """Основная функция"""
    print("=" * 80)
    print("РЕШЕНИЕ СИСТЕМЫ НЕЛИНЕЙНЫХ УРАВНЕНИЙ МЕТОДОМ ПОКООРДИНАТНОГО СПУСКА")
    print("=" * 80)
    
    # ЭТАП 1: Локализация
    x0 = localization_phase()
    
    # ЭТАП 2: Численное решение
    eps = 1e-6
    
    print("\n" + "=" * 80)
    print("ЭТАП 2: ЧИСЛЕННОЕ РЕШЕНИЕ МЕТОДОМ ПОКООРДИНАТНОГО СПУСКА")
    print("=" * 80)
    print(f"Начальное приближение: x0 = [{x0[0]:.2f}, {x0[1]:.2f}]")
    print(f"Точность: ε = {eps}")
    print("-" * 80)
    
    # Функция обратного вызова для вывода информации на каждой итерации
    def print_iteration(k, x, phi_val, grad_norm, diff_norm):
        if k == 0:
            print(f"{'Итерация':^8} | {'x1':^12} | {'x2':^12} | {'Φ(x)':^12} | {'||∇Φ||':^12} | {'Точность':^12}")
            print("-" * 80)
        print(f"{k+1:^8} | {x[0]:^12.6f} | {x[1]:^12.6f} | {phi_val:^12.6f} | {grad_norm:^12.6f} | {diff_norm:^12.6f}")
    
    solution, iterations, phi_val, grad_norm, eps, history = coordinate_descent(x0, eps, callback=print_iteration)
    
    print("=" * 80)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Решение: x* = [{solution[0]:.8f}, {solution[1]:.8f}]")
    print(f"Количество итераций: k = {iterations}")
    print(f"Значение функции: Φ(x*) = {phi_val:.8f}")
    print(f"Норма градиента: ||∇Φ|| = {grad_norm:.8f}")
    
    # Проверка
    print("-" * 40)
    print("ПРОВЕРКА СИСТЕМЫ:")
    f1_val = f1(solution[0], solution[1])
    f2_val = f2(solution[0], solution[1])
    print(f"f1(x) = {f1_val:.8f} (должно быть 0)")
    print(f"f2(x) = {f2_val:.8f} (должно быть 0)")
    
    # ЭТАП 3: Визуализация
    print("\n" + "=" * 80)
    print("ЭТАП 3: ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ")
    print("=" * 80)
    visualize_results(history, solution)

if __name__ == "__main__":
    main()