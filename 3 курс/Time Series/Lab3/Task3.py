import pandas as pd
import matplotlib.pyplot as plt

# Загружаем данные
df = pd.read_csv("lab3_data4.txt", sep="\t", header=None)
df.columns = ["Ничего", "Агрессивная", "Белый шум", "Классическая", "Ритмичная"]

# Преобразуем в бинарные данные
def to_binary(column):
    return (column < column.mean()).astype(int)

# Применяем функцию ко всем столбцам и переименовываем новые столбцы
binary_columns = {col: to_binary(df[col]) for col in df.columns}
df_binary = pd.DataFrame(binary_columns)
df_binary.columns = [f"{col}_binary" for col in df.columns]

# Ограничиваем датасет (например, первые 100 значений для лучшей визуализации)
df_cropped = df_binary.iloc[:100]

# Создаем график
plt.figure(figsize=(15, 6))  # Увеличим размер для наглядности

# Устанавливаем ширину баров
bar_width = 0.1

# Словарь для цветов и меток
colors_labels = {
    "Ничего_binary": ('blue', "Ничего"),
    "Агрессивная_binary": ('red', "Агрессивная"),
    "Белый шум_binary": ('green', "Белый шум"),
    "Классическая_binary": ('purple', "Классическая"),
    "Ритмичная_binary": ('orange', "Ритмичная"),
}

# Рисуем графики для каждого типа музыки
for column, (color, label) in colors_labels.items():
    plt.bar(df_cropped.index[df_cropped[column] == 1], [1] * len(df_cropped[df_cropped[column] == 1]), 
            color=color, width=bar_width, label=label, alpha=0.7)

# Добавляем элементы графика
plt.title("Изменение сердечного ритма под разную музыку", fontsize=16)
plt.xlabel("Время (мс)", fontsize=14)
plt.ylabel("Удар (1) / Отсутствие удара (0)", fontsize=14)
plt.ylim(0, 1.2)  # Устанавливаем пределы оси Y
plt.xlim(-1, len(df_cropped))  # Устанавливаем пределы оси X
plt.legend(fontsize=12)
plt.grid(True)
plt.show()
