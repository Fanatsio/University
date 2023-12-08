import matplotlib.pyplot as plt


def build_func(ground_speed, water_speed, x1, y1, x2, y2):
    def wrap(x):
        # Расчет времени для двух точек и их вкладов
        term1 = (1 / ground_speed) * ((x - x1) / ((x - x1)**2 + y1**2)**0.5)
        term2 = (1 / water_speed) * ((x - x2) / ((x - x2)**2 + y2**2)**0.5)
        # Общее время спасения
        return term1 + term2
    return wrap

# Функция, которая находит оптимальное значение методом средних отрезков
def find_optimal_x(ground_speed, water_speed, x1, y1, x2, y2):
    # Создание функции времени спасения
    func = build_func(ground_speed, water_speed, x1, y1, x2, y2)

    # Начальные границы поиска
    left_border, right_border = min(x1, x2), max(x1, x2)
    cur_x = (right_border + left_border) / 2

    while True:
        cur_v = func(cur_x)
        # Проверка на достижение достаточно малого значения
        if abs(cur_v) < 0.0000001:
            return cur_x

        # Коррекция границ поиска в зависимости от знака текущего времени спасения
        if cur_v > 0:
            right_border = cur_x
        else:
            left_border = cur_x

        # Вычисление нового значения x
        cur_x = (right_border + left_border) / 2

# Функция для визуализации сценария спасения
def show_graph(x, ground_speed, water_speed, x1, y1, x2, y2):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot([x1, x], [y1, 0], 'bo-')  # синяя линия от (x1, y1) к (0, 0)
    ax.plot([x, x2], [0, y2], 'ro-')  # красная линия от (0, 0) к (x2, y2)

    ax.text(x1, y1, f'({x1}, {y1})', fontsize=12, verticalalignment='bottom', horizontalalignment='right')
    ax.text(x2, y2, f'({x2}, {y2})', fontsize=12, verticalalignment='bottom', horizontalalignment='left')
    ax.text(x, 0, f'({x}, 0)', fontsize=12, verticalalignment='top', horizontalalignment='right')
    ax.text(0, -0.1, f"Скорость по земле: {ground_speed}\nСкорость по воде: {water_speed}", transform=ax.transAxes, ha="left", va="center")

    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Визуализация спасения')

    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.5)
    plt.axvline(0, color='black', linewidth=0.5)
    plt.grid(color='gray', linestyle='--', linewidth=0.5)
    plt.show()

def main():
    ground_speed, water_speed = 5, 1
    x1, y1 = 10, -10
    x2, y2 = 100, -15

    x = find_optimal_x(ground_speed, water_speed, x1, y1, x2, y2)
    show_graph(round(x, 4), ground_speed, water_speed, x1, y1, x2, y2)

if __name__ == "__main__":
    main()
