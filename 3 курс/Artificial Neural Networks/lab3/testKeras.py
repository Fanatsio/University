import numpy as np
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import SGD
from tensorflow.keras.initializers import RandomUniform
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.metrics import MeanSquaredError as MSE

# Загрузка данных
data = pd.read_csv('data/3lab_data.csv')
X = data[['x1', 'x2', 'x3']].values  # Входные данные
y = data[['y1', 'y2']].values  # Выходные данные

# Нормализация данных
X_max = np.max(X, axis=0)
y_max = np.max(y, axis=0)
X_normalized = X
y_normalized = y

# Создание модели
model = Sequential([
    Dense(3, input_dim=3, activation='sigmoid'),  # Первый скрытый слой с сигмоидой
    Dense(2, activation='sigmoid')                # Выходной слой с сигмоидой
])

# Компиляция модели
model.compile(optimizer='adam', loss='mse')

# Обучение модели
model.fit(X_normalized, y_normalized, epochs=500, verbose=1)

# Проверка результатов
predictions = model.predict(X)
print("Предсказания модели:")
print(predictions)
