import numpy as np
from functions import f1, f2, phi
from visualization import plot_localization_phase

def localization_phase():
    """Этап 1: Локализация минимума графическим методом"""
    print("=" * 80)
    print("ЭТАП 1: ЛОКАЛИЗАЦИЯ МИНИМУМА ГРАФИЧЕСКИМ МЕТОДОМ")
    print("=" * 80)
    
    # Создаем сетку
    x1 = np.linspace(-5, 8, 200)
    x2 = np.linspace(-4, 6, 200)
    X1, X2 = np.meshgrid(x1, x2)
    
    # Вычисляем значения
    F1 = f1(X1, X2)
    F2 = f2(X1, X2)
    PHI = phi([X1, X2])
    
    # Визуализация
    plot_localization_phase(X1, X2, F1, F2, PHI)
    
    # Анализ
    print("\nАНАЛИЗ ГРАФИКОВ:")
    print("-" * 40)
    print("1. По графикам f1=0 и f2=0 видно, что система имеет решение в области")
    print("   пересечения синей и красной линий.")
    print("2. Тепловая карта Φ(x) показывает области с наименьшими значениями")
    print("   (темные области на карте соответствуют минимумам).")

    candidate_points = [
        [0.0, 0.0],
        [2.0, 1.0],
        [3.0, 2.0],
        [1.0, -1.0]
    ]
    
    print("\nРЕКОМЕНДУЕМЫЕ НАЧАЛЬНЫЕ ПРИБЛИЖЕНИЯ:")
    print("-" * 40)
    print(f"{'№':^4} | {'x1':^10} | {'x2':^10} | {'Φ(x)':^12}")
    print("-" * 45)
    
    for i, point in enumerate(candidate_points, 1):
        phi_val = phi(point)
        print(f"{i:^4} | {point[0]:^10.2f} | {point[1]:^10.2f} | {phi_val:^12.6f}")
        if phi_val < 0.1:
            print(f"      ✓ Отличное начальное приближение! Φ(x) близко к 0")
    
    print("\n" + "=" * 80)
    
    best_point = min(candidate_points, key=lambda p: phi(p))
    print(f"Выбрано оптимальное начальное приближение: x0 = [{best_point[0]}, {best_point[1]}]")
    print("=" * 80)
    
    return best_point