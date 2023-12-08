from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# Загрузка изображения
image_path = "kotik.jpg"
image = Image.open(image_path)

# Преобразование изображения в массив numpy
image_array = np.array(image)

# Выбор цвета (например, желтый - 255, 255, 0)
our_color = np.array([255, 255, 0])

# Создание набора данных для обучения
training_data = []

# Выделение участков изображения
patch_size = 20
for i in range(0, image_array.shape[0] - patch_size, patch_size // 2):
    for j in range(0, image_array.shape[1] - patch_size, patch_size // 2):
        patch = image_array[i:i+patch_size, j:j+patch_size]
        if patch.size == 0:
            continue  # Пропускаем пустые участки
        is_our_color = np.array_equal(patch[patch_size // 2, patch_size // 2], our_color)
        training_data.append((patch.flatten(), int(is_our_color)))

# Создание нового изображения с выделенными участками цвета
highlighted_image = np.copy(image_array)

# Вывод данных
print("R\tG\tB\tour color?")
for data in training_data:
    print(f"{data[0][0]}\t{data[0][1]}\t{data[0][2]}\t{data[1]}")

# Визуализация изображения
plt.imshow(highlighted_image)
plt.show()