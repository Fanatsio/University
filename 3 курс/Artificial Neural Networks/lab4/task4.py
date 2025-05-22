import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
import tensorflow as tf

def sigm(x):
    return tf.sin(x)

X = np.arange(-20, 20, 0.1)
y = np.sin(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(Dense(64, input_dim=1, activation=sigm))
model.add(Dense(32, activation=sigm))
model.add(Dense(16, activation=sigm))
model.add(Dense(1, activation=sigm))

model.compile(loss='mean_squared_error', optimizer='adam')

# Список для сохранения значений функции потерь
history = []

# Обучение модели с сохранением истории
history = model.fit(X_train, y_train, epochs=50, batch_size=16, verbose=1)

# Получение предсказаний для всего диапазона значений X
y_pred = model.predict(X)

# Визуализация результатов
plt.figure(figsize=(12, 6))

# График функции потерь
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'])
plt.title('Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')

# График предсказаний и истинной функции
plt.subplot(1, 2, 2)
plt.scatter(X, y, color='black', label='Actual data')
plt.scatter(X, y_pred, color='red', label='Predicted data')
plt.plot(X, np.sin(X), color='blue', linewidth=3, label='True function')
plt.xlabel('X')
plt.ylabel('f(X)')
plt.legend()

plt.tight_layout()
plt.show()
