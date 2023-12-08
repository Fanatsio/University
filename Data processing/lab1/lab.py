import glob
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score


# pathNeg = "/home/maslenok/Рабочий стол/606-12 Демьянцев/lab1/data/movie/neg/"
# pathPos = "/home/maslenok/Рабочий стол/606-12 Демьянцев/lab1/data/movie/pos/"

pathNeg = "D:/Задания/2 семестр/python/машин. обучение/lab1/data/movie/neg"
pathPos = "D:/Задания/2 семестр/python/машин. обучение/lab1/data/movie/pos"
s1 = []
s2 = []

for filename in glob.glob(f"{pathNeg}/*.txt"):
    with open(filename, 'r') as f:
        words = f.readline()
        for i in words.split():
            s1.append(i)

# Загрузка данных из папки pathPos
for filename in glob.glob(f"{pathPos}/*.txt"):
    with open(filename, 'r') as f:
        words = f.readline()
        for i in words.split():
            s2.append(i)

s3 = s1 + s2

words = list(set(s3))

results = np.zeros((len(s3), len(words)))

for i, sequence in enumerate(s1):
    for j in sequence.split():
        results[i, words.index(j)] = 1

y = np.array([0] * (len(results) // 2) + [1] * (len(results) // 2 + 1))
X_train, X_test, Y_train, Y_test = train_test_split(results, y, test_size=0.2, random_state=5)

clf = BernoulliNB()
clf.fit(X_train, Y_train)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(Y_test, y_pred)
print(f'Точность модели: {accuracy:.2f}')
