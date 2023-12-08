from sklearn.linear_model import LinearRegression, LassoCV, RidgeCV
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import KFold

# Шаг 17: Обучение линейной регрессии
# Выбираем первые 1000 объектов
X_train_subset = X_train[:1000]
y_train_subset = y_train[:1000]
X_test_subset = X_test[:1000]
y_test_subset = y_test[:1000]

# Инициализация и обучение линейной регрессии
lr = LinearRegression()
lr.fit(X_train_subset, y_train_subset)

# Предсказание на обучающей и контрольной выборках
y_train_pred = lr.predict(X_train_subset)
y_test_pred = lr.predict(X_test_subset)

# Вычисление MSE и R^2
mse_train = mean_squared_error(y_train_subset, y_train_pred)
r2_train = r2_score(y_train_subset, y_train_pred)
mse_test = mean_squared_error(y_test_subset, y_test_pred)
r2_test = r2_score(y_test_subset, y_test_pred)

print(f"Linear Regression (no regularization):")
print(f"MSE on train: {mse_train}")
print(f"R^2 on train: {r2_train}")
print(f"MSE on test: {mse_test}")
print(f"R^2 on test: {r2_test}")

# Шаг 18: Обучение Lasso и Ridge регрессий с кросс-валидацией
# Задаем значения alpha для перебора
alpha_grid = [0.01, 0.1, 1, 10, 100]

# Lasso регрессия
lasso_cv = LassoCV(alphas=alpha_grid, cv=5)
lasso_cv.fit(X_train_subset, y_train_subset)
lasso_mse_train = mean_squared_error(y_train_subset, lasso_cv.predict(X_train_subset))
lasso_r2_train = lasso_cv.score(X_train_subset, y_train_subset)
lasso_mse_test = mean_squared_error(y_test_subset, lasso_cv.predict(X_test_subset))
lasso_r2_test = lasso_cv.score(X_test_subset, y_test_subset)

print("\nLasso Regression:")
print(f"Best alpha: {lasso_cv.alpha_}")
print(f"MSE on train: {lasso_mse_train}")
print(f"R^2 on train: {lasso_r2_train}")
print(f"MSE on test: {lasso_mse_test}")
print(f"R^2 on test: {lasso_r2_test}")

# Ridge регрессия
ridge_cv = RidgeCV(alphas=alpha_grid, cv=5)
ridge_cv.fit(X_train_subset, y_train_subset)
ridge_mse_train = mean_squared_error(y_train_subset, ridge_cv.predict(X_train_subset))
ridge_r2_train = ridge_cv.score(X_train_subset, y_train_subset)
ridge_mse_test = mean_squared_error(y_test_subset, ridge_cv.predict(X_test_subset))
ridge_r2_test = ridge_cv.score(X_test_subset, y_test_subset)

print("\nRidge Regression:")
print(f"Best alpha: {ridge_cv.alpha_}")
print(f"MSE on train: {ridge_mse_train}")
print(f"R^2 on train: {ridge_r2_train}")
print(f"MSE on test: {ridge_mse_test}")
print(f"R^2 on test: {ridge_r2_test}")
