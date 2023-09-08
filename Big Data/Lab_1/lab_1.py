import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score

# For Linux:
'''
pathNeg = "/home/maslenok/Рабочий стол/606-12/Речук/lab1/data/movie/neg/"
pathPos = "/home/maslenok/Рабочий стол/606-12/Речук/lab1/data/movie/pos/"
'''

# For Windows:
pathNeg = "D:/GitHub/University/Big Data/Lab_1/data/movie/neg/"
pathPos = "D:/GitHub/University/Big Data/Lab_1/data/movie/pos/"

pos = os.listdir(pathNeg)
neg = os.listdir(pathPos)
s1 = []
s2 = []

os.chdir(pathNeg)
for _ in pos:
    with open(_, 'r') as f:
        words = f.readline()
        for i in words.split():
            s1.append(i)

os.chdir(pathPos)
for _ in neg:
    with open(_, 'r') as f:
        words = f.readline()
        for i in words.split():
            s2.append(i)

s3 = []
s3.extend(s1)
s3.extend(s2)

words = list(set(s3))

results = np.zeros((len(s3), len(words)))

for i, sequence in enumerate(s1):
    for j in sequence.split():
        results[i, words.index(j)] = 1

y = np.array([0] * (len(results) // 2) + [1] * (len(results) // 2 + 1))
X_train, X_test, Y_train, Y_test = train_test_split(results, y, test_size=0.2, random_state=0)

clf = BernoulliNB()
clf.fit(X_train, Y_train)
y_pred = clf.predict(X_test)
accuracy = accuracy_score(Y_test, y_pred)

print(f'Model Accuracy: {accuracy:.2f}')
