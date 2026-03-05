import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def f1(x1, x2):
    """Первое уравнение системы: sin(0.2x2) - cos(0.4x1) = -0.1"""
    return np.sin(0.2 * x2) - np.cos(0.4 * x1) + 0.1

def f2(x1, x2):
    """Второе уравнение системы: e^(-((x1-2)/4)^2) * e^(-((x2-1)/3)^2) = 0.1"""
    return np.exp(-((x1 - 2) / 4) ** 2) * np.exp(-((x2 - 1) / 3) ** 2) - 0.1

def phi(x):
    """Целевая функция Ф(x,y) = f1^2 + f2^2"""
    x1, x2 = x[0], x[1]
    return f1(x1, x2)**2 + f2(x1, x2)**2

def gradient(x, h=1e-6):
    """Вычисление градиента численным методом"""
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_minus = x.copy()
        x_plus[i] += h
        x_minus[i] -= h
        grad[i] = (phi(x_plus) - phi(x_minus)) / (2 * h)
    return grad

def localization_phase():
    """
    Этап 1: Локализация минимума графическим методом
    """
    print("=" * 80)
    print("ЭТАП 1: ЛОКАЛИЗАЦИЯ МИНИМУМА ГРАФИЧЕСКИМ МЕТОДОМ")
    print("=" * 80)
    
    # Создаем сетку для анализа
    x1 = np.linspace(-5, 8, 200)
    x2 = np.linspace(-4, 6, 200)
    X1, X2 = np.meshgrid(x1, x2)
    
    # Вычисляем значения функций на сетке
    F1 = f1(X1, X2)
    F2 = f2(X1, X2)
    PHI = phi([X1, X2])
    
    # Создаем фигуру с несколькими подграфиками
    fig = plt.figure(figsize=(16, 10))
    
    # 1. График f1(x1,x2) = 0 (неявная функция)
    ax1 = fig.add_subplot(221)
    contour1 = ax1.contour(X1, X2, F1, levels=[0], colors='blue', linewidths=2)
    ax1.clabel(contour1, inline=True, fontsize=10)
    ax1.contour(X1, X2, F1, levels=20, colors='lightblue', alpha=0.5, linestyles='dashed')
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_title('Линии уровня f1(x1,x2) = 0 (синяя)')
    ax1.grid(True, alpha=0.3)
    
    # 2. График f2(x1,x2) = 0 (неявная функция)
    ax2 = fig.add_subplot(222)
    contour2 = ax2.contour(X1, X2, F2, levels=[0], colors='red', linewidths=2)
    ax2.clabel(contour2, inline=True, fontsize=10)
    ax2.contour(X1, X2, F2, levels=20, colors='lightcoral', alpha=0.5, linestyles='dashed')
    ax2.set_xlabel('x1')
    ax2.set_ylabel('x2')
    ax2.set_title('Линии уровня f2(x1,x2) = 0 (красная)')
    ax2.grid(True, alpha=0.3)
    
    # 3. Совмещенный график - пересечение функций
    ax3 = fig.add_subplot(223)
    contour1_3 = ax3.contour(X1, X2, F1, levels=[0], colors='blue', linewidths=2, label='f1=0')
    contour2_3 = ax3.contour(X1, X2, F2, levels=[0], colors='red', linewidths=2, label='f2=0')
    # Добавим линии уровня Ф(x) для контекста
    contour_phi = ax3.contour(X1, X2, PHI, levels=20, cmap='viridis', alpha=0.6)
    ax3.set_xlabel('x1')
    ax3.set_ylabel('x2')
    ax3.set_title('Пересечение f1=0 (синий) и f2=0 (красный)')
    ax3.grid(True, alpha=0.3)
    # Создаем легенду вручную
    from matplotlib.lines import Line2D
    legend_elements = [Line2D([0], [0], color='blue', lw=2, label='f1(x) = 0'),
                       Line2D([0], [0], color='red', lw=2, label='f2(x) = 0')]
    ax3.legend(handles=legend_elements, loc='upper right')
    
    # 4. Тепловая карта Φ(x) с указанием минимумов
    ax4 = fig.add_subplot(224)
    # Найдем несколько точек с минимальными значениями Φ для ориентира
    min_idx = np.unravel_index(np.argmin(PHI, axis=None), PHI.shape)
    min_x1, min_x2 = X1[min_idx], X2[min_idx]
    
    im = ax4.imshow(PHI, extent=[x1.min(), x1.max(), x2.min(), x2.max()], 
                   origin='lower', cmap='viridis', aspect='auto', alpha=0.8)
    plt.colorbar(im, ax=ax4, label='Φ(x)')
    ax4.contour(X1, X2, PHI, levels=20, colors='white', alpha=0.5, linewidths=0.5)
    ax4.plot(min_x1, min_x2, 'r*', markersize=15, label='Глобальный минимум на сетке')
    ax4.set_xlabel('x1')
    ax4.set_ylabel('x2')
    ax4.set_title('Тепловая карта Φ(x) = f1² + f2²')
    ax4.legend()
    
    plt.tight_layout()
    plt.show()
    
    # Анализ и рекомендации по выбору начального приближения
    print("\nАНАЛИЗ ГРАФИКОВ:")
    print("-" * 40)
    print("1. По графикам f1=0 и f2=0 видно, что система имеет решение в области")
    print("   пересечения синей и красной линий.")
    print("2. Тепловая карта Φ(x) показывает области с наименьшими значениями")
    print("   (темные области на карте соответствуют минимумам).")
    
    # Предлагаем несколько вариантов начальных приближений
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
        if phi_val < 0.1:  # Если значение уже близко к нулю
            print(f"      ✓ Отличное начальное приближение! Φ(x) близко к 0")
    
    print("\n" + "=" * 80)
    
    # Возвращаем лучшее начальное приближение (с минимальным Φ)
    best_point = min(candidate_points, key=lambda p: phi(p))
    print(f"Выбрано оптимальное начальное приближение: x0 = [{best_point[0]}, {best_point[1]}]")
    print("=" * 80)
    
    return best_point

def coordinate_descent(x0, eps=1e-6, max_iter=1000):
    """
    Метод покоординатного спуска
    """
    x = np.array(x0, dtype=float)
    history = [x.copy()]
    k = 0
    
    print(f"\n{'Итерация':^8} | {'x1':^12} | {'x2':^12} | {'Φ(x)':^12} | {'||∇Φ||':^12} | {'Точность':^12}")
    print("-" * 80)
    
    while k < max_iter:
        x_prev = x.copy()
        
        # Цикл по координатам
        for i in range(len(x)):
            # Минимизация по i-ой координате методом золотого сечения
            def phi_i(alpha):
                x_temp = x.copy()
                x_temp[i] = alpha
                return phi(x_temp)
            
            # Определяем интервал для поиска (адаптивный)
            step = 1.0
            a, b = x[i] - step, x[i] + step
            
            # Расширяем интервал, если минимум на границах
            for _ in range(5):
                if phi_i(a) < phi_i(x[i]) or phi_i(b) < phi_i(x[i]):
                    step *= 2
                    a, b = x[i] - step, x[i] + step
                else:
                    break
            
            # Метод золотого сечения для одномерной минимизации
            tau = (np.sqrt(5) - 1) / 2
            c = b - tau * (b - a)
            d = a + tau * (b - a)
            
            # Внутренняя точность для золотого сечения
            inner_eps = eps / 10
            
            while abs(b - a) > inner_eps:
                if phi_i(c) < phi_i(d):
                    b = d
                else:
                    a = c
                
                c = b - tau * (b - a)
                d = a + tau * (b - a)
            
            x[i] = (a + b) / 2
        
        # Вычисляем норму разности и градиент
        diff_norm = np.linalg.norm(x - x_prev)
        grad = gradient(x)
        grad_norm = np.linalg.norm(grad)
        
        # Выводим информацию на каждой итерации
        print(f"{k+1:^8} | {x[0]:^12.6f} | {x[1]:^12.6f} | {phi(x):^12.6f} | {grad_norm:^12.6f} | {diff_norm:^12.6f}")
        
        history.append(x.copy())
        
        # Проверка критерия выхода
        if diff_norm < eps:
            break
            
        k += 1
    
    return x, k+1, phi(x), grad_norm, eps, np.array(history)

def visualize_results(history, solution):
    """Визуализация процесса минимизации"""
    # Создаем сетку для построения поверхности
    x1 = np.linspace(-2, 6, 100)
    x2 = np.linspace(-2, 4, 100)
    X1, X2 = np.meshgrid(x1, x2)
    Z = np.zeros_like(X1)
    
    for i in range(len(x1)):
        for j in range(len(x2)):
            Z[j, i] = phi([X1[j, i], X2[j, i]])
    
    # Построение 3D графика
    fig = plt.figure(figsize=(15, 5))
    
    # 3D поверхность
    ax1 = fig.add_subplot(131, projection='3d')
    surf = ax1.plot_surface(X1, X2, Z, cmap='viridis', alpha=0.8)
    ax1.scatter(history[:, 0], history[:, 1], 
                [phi(x) for x in history], color='red', s=50)
    ax1.plot(history[:, 0], history[:, 1], 
             [phi(x) for x in history], 'r-', linewidth=1, alpha=0.7)
    ax1.set_xlabel('x1')
    ax1.set_ylabel('x2')
    ax1.set_zlabel('Φ(x)')
    ax1.set_title('Траектория минимизации')
    plt.colorbar(surf, ax=ax1, shrink=0.5)
    
    # 2D контурный график
    ax2 = fig.add_subplot(132)
    contour = ax2.contour(X1, X2, Z, levels=50, cmap='viridis')
    ax2.plot(history[:, 0], history[:, 1], 'r.-', linewidth=2, markersize=8)
    ax2.plot(solution[0], solution[1], 'g*', markersize=15, label='Найденный минимум')
    ax2.plot(history[0, 0], history[0, 1], 'bo', markersize=8, label='Начальное приближение')
    ax2.set_xlabel('x1')
    ax2.set_ylabel('x2')
    ax2.set_title('Траектория на контурной карте')
    ax2.legend()
    plt.colorbar(contour, ax=ax2)
    
    # График сходимости
    ax3 = fig.add_subplot(133)
    phi_values = [phi(x) for x in history]
    ax3.semilogy(range(len(phi_values)), phi_values, 'b.-')
    ax3.set_xlabel('Итерация')
    ax3.set_ylabel('Φ(x)')
    ax3.set_title('Сходимость метода')
    ax3.grid(True)
    
    plt.tight_layout()
    plt.show()

def main():
    """Основная функция"""
    print("=" * 80)
    print("РЕШЕНИЕ СИСТЕМЫ НЕЛИНЕЙНЫХ УРАВНЕНИЙ МЕТОДОМ ПОКООРДИНАТНОГО СПУСКА")
    print("=" * 80)
    
    # ЭТАП 1: Локализация минимума графическим методом
    x0 = localization_phase()
    
    # ЭТАП 2: Численное решение
    eps = 1e-6
    
    print("\n" + "=" * 80)
    print("ЭТАП 2: ЧИСЛЕННОЕ РЕШЕНИЕ МЕТОДОМ ПОКООРДИНАТНОГО СПУСКА")
    print("=" * 80)
    print(f"Начальное приближение: x0 = [{x0[0]:.2f}, {x0[1]:.2f}]")
    print(f"Точность: ε = {eps}")
    print("-" * 80)
    
    # Запуск метода
    solution, iterations, phi_val, grad_norm, eps, history = coordinate_descent(x0, eps)
    
    print("=" * 80)
    print("РЕЗУЛЬТАТЫ:")
    print(f"Решение: x* = [{solution[0]:.8f}, {solution[1]:.8f}]")
    print(f"Количество итераций: k = {iterations}")
    print(f"Значение функции: Φ(x*) = {phi_val:.8f}")
    print(f"Норма градиента: ||∇Φ|| = {grad_norm:.8f}")
    print(f"Достигнутая точность: ε = {eps}")
    
    # Проверка выполнения системы уравнений
    print("-" * 40)
    print("ПРОВЕРКА СИСТЕМЫ:")
    f1_val = f1(solution[0], solution[1])
    f2_val = f2(solution[0], solution[1])
    print(f"f1(x) = {f1_val:.8f} (должно быть 0)")
    print(f"f2(x) = {f2_val:.8f} (должно быть 0)")
    
    # ЭТАП 3: Визуализация результатов
    print("\n" + "=" * 80)
    print("ЭТАП 3: ВИЗУАЛИЗАЦИЯ РЕЗУЛЬТАТОВ")
    print("=" * 80)
    visualize_results(history, solution)

if __name__ == "__main__":
    main()