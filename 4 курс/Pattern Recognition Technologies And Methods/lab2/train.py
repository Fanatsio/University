import numpy as np
import cv2
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib  # для сохранения модели на диск

# Пример извлечения признаков HOG (этот код можно адаптировать под ваши данные)
def extract_hog_features(image):
    gray_image = rgb2gray(image)  # Преобразуем изображение в оттенки серого
    features, hog_image = hog(gray_image, pixels_per_cell=(8, 8),
                              cells_per_block=(2, 2), visualize=True, feature_vector=True)
    return features

# Предполагаем, что у нас есть данные и метки
features = []  # Ваши извлеченные признаки
labels = []    # Метки (1 - кот, 0 - не кот)

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

# Обучаем SVM (или можно использовать любую другую модель)
svm = SVC(kernel='linear')
svm.fit(X_train, y_train)

# Оцениваем точность на обучающем наборе
y_pred = svm.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Точность на тестовом наборе: {accuracy:.2f}")

# Сохраняем модель на диск
joblib.dump(svm, 'svm_cat_classifier.pkl')  # Сохраняем модель в файл
print("Модель сохранена как 'svm_cat_classifier.pkl'")
