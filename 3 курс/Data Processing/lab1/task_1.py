import glob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, mean_squared_error
from sklearn.feature_extraction.text import CountVectorizer

pathNeg = "./data/movie/neg"
pathPos = "./data/movie/pos"

def openFile(path: str) -> list:
    array = []
    for filename in glob.glob(f"{path}/*.txt"):
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            array.append(content)
    return array

neg_list = openFile(pathNeg)
pos_list = openFile(pathPos)

# Объединяем списки негативных и позитивных отзывов
all_list = neg_list + pos_list

# Создаем векторизатор
vectorizer = CountVectorizer(binary=True)
results = vectorizer.fit_transform(all_list).toarray()

# Создаем метки для классов
y = np.array([0] * len(neg_list) + [1] * len(pos_list))

# Разбиваем данные на обучающую и тестовую выборки
X_train, X_test, Y_train, Y_test = train_test_split(results, y, test_size=0.2, random_state=0)

# Создаем и обучаем классификатор
clf = BernoulliNB()
clf.fit(X_train, Y_train)

# Оцениваем модель
accuracy = accuracy_score(clf.predict(X_test), Y_test)
print(f'Model accuracy: {accuracy}')

y_pred = clf.predict(X_test)

# Рассчитываем среднеквадратичную ошибку
mse = mean_squared_error(Y_test, y_pred)
print(f'Mean squared error: {mse:.2f}')
