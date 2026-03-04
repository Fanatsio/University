import numpy as np

# Система уравнений, приведенная к виду F(x) = 0
def F(x):
    x1, x2 = x
    f1 = np.sin(0.2 * x2) - np.cos(0.4 * x1) + 0.1
    f2 = np.exp(-((x1 - 2) / 4)**2) * np.exp(-((x2 - 1) / 3)**2) - 0.1
    return np.array([f1, f2])

# Якобиан (матрица производных)
def J(x):
    x1, x2 = x

    df1_dx1 = 0.4 * np.sin(0.4 * x1)
    df1_dx2 = 0.2 * np.cos(0.2 * x2)

    exp_part = np.exp(-((x1 - 2) / 4)**2) * np.exp(-((x2 - 1) / 3)**2)
    df2_dx1 = exp_part * (- (x1 - 2) / 8)
    df2_dx2 = exp_part * (- 2 * (x2 - 1) / 9)

    return np.array([
        [df1_dx1, df1_dx2],
        [df2_dx1, df2_dx2]
    ])

# Неявный метод Ньютона с улучшенной диагностикой
def newton_system(x0, eps=1e-6, max_iter=50):
    x = np.array(x0, dtype=float)
    iter_count = 0
    
    for i in range(max_iter):
        Fx = F(x)
        Jx = J(x)
        
        # Проверка на вырожденность
        det = np.linalg.det(Jx)
        if abs(det) < 1e-12:
            return None, i, f"Вырожденная матрица (det = {det:.2e})"
        
        try:
            delta = np.linalg.solve(Jx, Fx)
        except np.linalg.LinAlgError:
            return None, i, "Ошибка решения СЛАУ"
        
        x_new = x - delta
        error = np.linalg.norm(x_new - x)
        
        if error < eps:
            return x_new, i + 1, f"Сошлось за {i+1} итераций"
        
        x = x_new
    
    return None, max_iter, f"Достигнут лимит итераций ({max_iter})"

# Функция для автоматического подбора начального приближения
def find_solution_with_grid_search(x1_range, x2_range, num_points=10):
    """
    Поиск решения перебором по сетке начальных приближений
    
    Parameters:
    x1_range: tuple (min, max) диапазон для x1
    x2_range: tuple (min, max) диапазон для x2
    num_points: количество точек по каждой координате
    """
    x1_values = np.linspace(x1_range[0], x1_range[1], num_points)
    x2_values = np.linspace(x2_range[0], x2_range[1], num_points)
    
    solutions = []
    
    print("=" * 70)
    print("ПОИСК РЕШЕНИЯ ПЕРЕБОРОМ НАЧАЛЬНЫХ ПРИБЛИЖЕНИЙ")
    print("=" * 70)
    print(f"Диапазон x1: [{x1_range[0]:.1f}, {x1_range[1]:.1f}], точек: {num_points}")
    print(f"Диапазон x2: [{x2_range[0]:.1f}, {x2_range[1]:.1f}], точек: {num_points}")
    print(f"Всего комбинаций: {num_points * num_points}")
    print("-" * 70)
    
    total_attempts = 0
    successful = 0
    
    for x1 in x1_values:
        for x2 in x2_values:
            x0 = [x1, x2]
            total_attempts += 1
            
            solution, iterations, message = newton_system(x0)
            
            if solution is not None:
                successful += 1
                Fx = F(solution)
                norm_F = np.linalg.norm(Fx)
                
                solutions.append({
                    'x0': x0.copy(),
                    'solution': solution.copy(),
                    'iterations': iterations,
                    'F_norm': norm_F,
                    'F_value': Fx.copy()
                })
                
                print(f"✅ Найдено! x0=[{x1:.3f}, {x2:.3f}] -> решение=[{solution[0]:.6f}, {solution[1]:.6f}], итер={iterations}, |F|={norm_F:.2e}")
            else:
                print(f"❌ Не сошлось: x0=[{x1:.3f}, {x2:.3f}] -> {message}")
    
    print("-" * 70)
    print(f"Всего попыток: {total_attempts}")
    print(f"Успешных решений: {successful}")
    
    if successful > 0:
        # Находим лучшее решение (минимальная норма невязки)
        best = min(solutions, key=lambda s: s['F_norm'])
        
        print("\n" + "=" * 70)
        print("ЛУЧШЕЕ НАЙДЕННОЕ РЕШЕНИЕ")
        print("=" * 70)
        print(f"Начальное приближение: [{best['x0'][0]:.6f}, {best['x0'][1]:.6f}]")
        print(f"Решение x: [{best['solution'][0]:.12f}, {best['solution'][1]:.12f}]")
        print(f"Количество итераций: {best['iterations']}")
        print(f"Норма невязки |F(x)|: {best['F_norm']:.2e}")
        print(f"F(x) = [{best['F_value'][0]:.2e}, {best['F_value'][1]:.2e}]")
        
        # Проверяем, насколько хорошо выполняется исходная система
        print("\nПРОВЕРКА ИСХОДНОЙ СИСТЕМЫ:")
        x1, x2 = best['solution']
        print(f"Уравнение 1: sin(0.2*{x2:.6f}) - cos(0.4*{x1:.6f}) = {np.sin(0.2*x2) - np.cos(0.4*x1):.8f} (должно быть -0.1)")
        print(f"Уравнение 2: exp(-(({x1:.6f}-2)/4)^2) * exp(-(({x2:.6f}-1)/3)^2) = {np.exp(-((x1-2)/4)**2) * np.exp(-((x2-1)/3)**2):.8f} (должно быть 0.1)")
        
        return best['solution']
    else:
        print("\n❌ Решений не найдено. Попробуйте расширить диапазоны поиска.")
        return None

if __name__ == "__main__":
    x1_range = [0.0, 4.0]   # диапазон для x1
    x2_range = [-1.0, 3.0]   # диапазон для x2

    print("ЭТАП 1: Грубый поиск (10x10)")
    solution = find_solution_with_grid_search(x1_range, x2_range, num_points=10)
    
    if solution is not None:
        # Если нашли решение, уточняем его с более высокой точностью
        print("\n\n" + "=" * 70)
        print("ЭТАП 2: Уточнение найденного решения с высокой точностью")
        print("=" * 70)
        
        # Используем найденное решение как начальное приближение
        x0 = solution.tolist() if isinstance(solution, np.ndarray) else solution
        final_solution, iterations, message = newton_system(x0, eps=1e-10)
        
        if final_solution is not None:
            print(f"\nОкончательное решение с точностью 1e-10:")
            print(f"x = [{final_solution[0]:.12f}, {final_solution[1]:.12f}]")
            print(f"Итераций: {iterations}")
            print(f"F(x) = {F(final_solution)}")
            print(f"|F(x)| = {np.linalg.norm(F(final_solution)):.2e}")
        else:
            print("Не удалось уточнить решение")
