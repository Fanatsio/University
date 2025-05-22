from keras.datasets import boston_housing
from sklearn.linear_model import Ridge

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()
mean = train_data.mean(axis=0)
train_data -= mean
std = train_data.std(axis=0)
train_data /= std

test_data -= mean
test_data /= std

model = Ridge()
model.fit(train_data, train_targets)
print(model.score(test_data, test_targets))