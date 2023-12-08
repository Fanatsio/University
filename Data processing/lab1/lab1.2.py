import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score


# pathNeg = "/home/maslenok/Рабочий стол/606-12/606-12 Демьянцев/MachLearn/lab1/data/movie/neg"
# pathPos = "/home/maslenok/Рабочий стол/606-12/606-12 Демьянцев/MachLearn/lab1/data/movie/pos"

pathNeg = "D:/Задания/3 курс/python/машин. обучение/lab1/data/movie/neg"
pathPos = "D:/Задания/3 курс/python/машин. обучение/lab1/data/movie/pos"
pos_texts = ''
neg_texts = ''
sep = ' '
neg = os.listdir(pathNeg)
pos = os.listdir(pathPos)

os.chdir(pathPos)
for _ in pos:
    with open(_, 'r') as f:
        pos_texts += sep.join(f.read())

os.chdir(pathNeg)
for _ in neg:
    with open(_, 'r') as f:
        neg_texts += sep.join(f.read())

all_texts = [pos_texts, neg_texts]
words = list(set((pos_texts+' '+neg_texts).split()))
results = np.zeros((len(all_texts), len(words)))
print(len(pos_texts))
print(len(neg_texts))
print(len(all_texts))
print(len(words))
print(len(results))

for i, sequence in enumerate(all_texts):
    for j in sequence.split():
        results[i, words.index(j)] = 1

y = np.array([0] * (len(results) // 2) + [1] * (len(results) // 2))
print(results)

X_train, X_test, Y_train, Y_test = train_test_split(results, y, test_size=0.2, random_state=0)

clf = BernoulliNB()
clf.fit(X_train, Y_train)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(Y_test, y_pred)
print(f'Точность модели: {accuracy:.2f}')