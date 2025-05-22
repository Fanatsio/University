from PIL import Image
import numpy as np
import pandas as pd
from neural_network import create_neural_network, train_neural_network, split_data, evaluate_neural_network

image = Image.open('./lab2/4/kotik.jpg')
pixel_colors = np.array(image)

target_color = np.array([242, 158, 194])

def is_target_color(color):
    return np.all(np.abs(color - target_color) < 20)

mask_target_color = np.array([[is_target_color(color) for color in row] for row in pixel_colors])
pixels_with_target_color = pixel_colors[mask_target_color]
pixels_without_target_color = pixel_colors[~mask_target_color]

# Создаем копию изображения. Отмечаем пиксели, соответствующие целевому цвету, остальные делаем черными
output_image = np.zeros_like(pixel_colors)
output_image[mask_target_color] = pixel_colors[mask_target_color]
output_image = Image.fromarray(output_image.astype('uint8'))
output_image.save('output_image.jpg')

# Создание датасета для обучения
df_with_target_color = pd.DataFrame(pixels_with_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_with_target_color['our color'] = 1

df_without_target_color = pd.DataFrame(pixels_without_target_color.reshape(-1, 3), columns=['R', 'G', 'B'])
df_without_target_color['our color'] = 0

training_data = pd.concat([df_with_target_color, df_without_target_color], ignore_index=True)

# Перетасовка датасета
shuffled_training_data = training_data.sample(frac=1).reset_index(drop=True)

print(training_data)
print(shuffled_training_data)

# Нормализуем данные
shuffled_training_data[['R', 'G', 'B']] = training_data[['R', 'G', 'B']] / 255.0

# Преобразуем датасет в формат, подходящий для обучения
shuffled_training_data_array = np.array(shuffled_training_data[['R', 'G', 'B']])
print(shuffled_training_data_array)
target_labels = np.array(shuffled_training_data['our color'])

train_data, test_data = split_data(list(zip(shuffled_training_data_array, target_labels)), train_fraction=0.8)

neural_net = create_neural_network(1, 3)

print(neural_net.neurons[0].get_weights())

evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)

train_neural_network(neural_net, train_data, learning_rate=0.001, epochs=10)

print(neural_net.neurons[0].get_weights())

evaluate_neural_network(neural_net, test_data)
evaluate_neural_network(neural_net, train_data)
