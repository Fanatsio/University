import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn import metrics

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
posList = []
negList = []

os.chdir(pathNeg)
for _ in pos:
    with open(_, 'r') as f:
        words = f.readline()
        for i in words.split():
            posList.append(i)

os.chdir(pathPos)
for _ in neg:
    with open(_, 'r') as f:
        words = f.readline()
        for i in words.split():
            negList.append(i)

s3 = []
s3.extend(posList)
s3.extend(negList)

words = list(set(s3))

results = np.zeros((len(s3), len(words)))

posListDig = np.zeros((len(posList), len(words)))
negListDig = np.zeros((len(negList), len(words)))

for i in range(len(posListDig)):
    posListDig[i] = 1

for i, sequence in enumerate(posList):
    for j in sequence.split():
        results[i, words.index(j)] = 1

print("res = ", results)
print("\npos = ", posListDig)
print("\nneg = ", negListDig)

#X_train, X_test, Y_train, Y_test = train_test_split( , , test_size=0.2, random_state=0)

'''
clf = BernoulliNB()
clf.fit()
metrics.accuracy_score()
'''
