import os
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import mean_squared_error

# For Linux:
'''
pathNeg = "/home/maslenok/Рабочий стол/606-12/Речук/lab1/data/movie/neg/"
pathPos = "/home/maslenok/Рабочий стол/606-12/Речук/lab1/data/movie/pos/"
'''

pathNeg = "D:/GitHub/University/Big Data/Lab_1/data/movie/neg/"
pathPos = "D:/GitHub/University/Big Data/Lab_1/data/movie/pos/"


def read_files_from_folder(folder_path):
    texts = []
    for filename in os.listdir(folder_path):
        with open(os.path.join(folder_path, filename), 'r') as file:
            texts.append(file.read())
    return texts


neg_texts = read_files_from_folder(pathNeg)
pos_texts = read_files_from_folder(pathPos)

all_texts = neg_texts + pos_texts

y = np.array([0] * len(neg_texts) + [1] * len(pos_texts))

vectorized = CountVectorizer(binary=True, max_features=5000)
X = vectorized.fit_transform(all_texts)

X_train, X_test, Y_train, Y_test = train_test_split(X, y, test_size=0.2, random_state=5)
clf = BernoulliNB()
clf.fit(X_train, Y_train)

y_pred = clf.predict(X_test)

accuracy = accuracy_score(Y_test, y_pred)
print(f'Model accuracy: {accuracy:.2f}')

mse = mean_squared_error(Y_test, y_pred)
print(f'Mean square error: {mse:.2f}')
