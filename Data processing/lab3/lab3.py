import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

import pandas as pd

import numpy as np

#1
def max_element(arr):
    zero_indices = np.where(arr[:-1] == 0)[0]
    if len(zero_indices) == 0:
        return None
    max_after_zero = np.max(arr[zero_indices + 1])
    return max_after_zero

# Пример использования:
x = np.array([6, 2, 0, 3, 0, 0, 5, 7, 0])
result = max_element(x)
print(result)  # Вывод: 5

#2
def nearest_value(X, v):
    flattened_X = X.flatten()
    index = np.argmin(np.abs(flattened_X - v))
    return flattened_X[index]

# Пример использования:
X = np.arange(0, 10).reshape((2, 5))
v = 3.6
result = nearest_value(X, v)
print(result)  # Вывод: 4

#3
def scale(X):
    means = np.mean(X, axis=0)
    stds = np.std(X, axis=0)
    scaled_X = (X - means) / np.where(stds == 0, 1, stds)  # Предотвращение деления на ноль
    return scaled_X

# Пример использования:
random_matrix = np.random.randint(0, 10, size=(3, 4))
scaled_matrix = scale(random_matrix)
print(scaled_matrix)

#4
def get_stats(X):
    determinant = np.linalg.det(X)
    trace = np.trace(X)
    min_element = np.min(X)
    max_element = np.max(X)
    frobenius_norm = np.linalg.norm(X, 'fro')
    eigenvalues = np.linalg.eigvals(X)

    try:
        inverse_matrix = np.linalg.inv(X)
    except np.linalg.LinAlgError:
        inverse_matrix = None

    return {
        'determinant': determinant,
        'trace': trace,
        'min_element': min_element,
        'max_element': max_element,
        'frobenius_norm': frobenius_norm,
        'eigenvalues': eigenvalues,
        'inverse_matrix': inverse_matrix
    }


# Пример использования:
random_matrix = np.random.randn(3, 3)
stats = get_stats(random_matrix)
for key, value in stats.items():
    print(f'{key}: {value}')


#5
max_elements = []

for exp_num in range(100):
    # Генерация двух матриц 10x10 из стандартного нормального распределения
    matrix1 = np.random.randn(10, 10)
    matrix2 = np.random.randn(10, 10)

    # Перемножение матриц
    result_matrix = np.dot(matrix1, matrix2)

    # Нахождение максимального элемента
    max_element = np.max(result_matrix)

    max_elements.append(max_element)

# Вычисление среднего значения и 95-процентной квантили
mean_max_element = np.mean(max_elements)
quantile_95 = np.percentile(max_elements, 95)

print(f'Среднее значение максимальных элементов: {mean_max_element}')
print(f'95-процентная квантиль максимальных элементов: {quantile_95}')

# Загрузка данных
df = pd.read_csv('airline_dec_2008_50k.csv')

# 6. Самая частая причина отмены рейса
most_common_cancellation_code = df['CancellationCode'].mode().values[0]
print(f'Самая частая причина отмены рейса: {most_common_cancellation_code}')

# 7. Среднее, минимальное и максимальное расстояние
mean_distance = df['Distance'].mean()
min_distance = df['Distance'].min()
max_distance = df['Distance'].max()
print(f'Среднее расстояние: {mean_distance}')
print(f'Минимальное расстояние: {min_distance}')
print(f'Максимальное расстояние: {max_distance}')

# 8. Подозрительное минимальное расстояние
suspicious_flights = df[df['Distance'] == min_distance]

print('Подозрительное минимальное расстояние:')
print(suspicious_flights)

# Расстояние для тех же рейсов в другие дни
other_days_distance = df[(df['UniqueCarrier'].isin(suspicious_flights['UniqueCarrier'])) & (df['Distance'] != min_distance)]
print('Расстояние для тех же рейсов в другие дни:')
print(other_days_distance)

# 9. Аэропорт с максимальным количеством вылетов
most_departures_airport = df['Origin'].value_counts().idxmax()
print(f'Аэропорт с максимальным количеством вылетов: {most_departures_airport}')

# 10. Аэропорт с наибольшим средним временем полета
max_avg_airtime_airport = df.groupby('Origin')['AirTime'].mean().idxmax()
print(f'Аэропорт с наибольшим средним временем полета: {max_avg_airtime_airport}')

# 11. Аэропорт с наибольшей долей задержанных рейсов
filtered_airports = df.groupby('Origin').filter(lambda x: len(x) >= 1000)
delayed_ratio_airport = filtered_airports.groupby('Origin')['DepDelay'].apply(lambda x: (x > 0).mean()).idxmax()
print(f'Аэропорт с наибольшей долей задержанных рейсов: {delayed_ratio_airport}')

# Шаг 12: Загрузка данных
# Указываем тип для избежания предупреждений о смешанных типах
dtype = {'CancellationCode': str}
df = pd.read_csv('airline_dec_2008_50k.csv', dtype=dtype, low_memory=False)

# Проверка наличия пропущенных значений
print(df.isnull().any().any())  # Имеются ли в данных пропущенные значения?
print(df.isnull().sum().sum())  # Сколько всего пропущенных элементов в таблице "объект-признак"?
print(df.isnull().any(axis=1).sum())  # Сколько объектов имеют хотя бы один пропуск?
print(df.isnull().any().sum())  # Сколько признаков имеют хотя бы одно пропущенное значение?

# Шаг 13: Обработка пропущенных значений в целевой переменной
df = df.dropna(subset=['DepDelay'])


# Шаг 13: Преобразование признаков времени
def extract_hour_minute(df, feature_name):
    df[feature_name + '_Hour'] = df[feature_name] // 100
    df[feature_name + '_Minute'] = df[feature_name] % 100
    df = df.drop(feature_name, axis=1)
    return df

import pandas as pd
import numpy as np

# Считывание данных из файла
dtype = {'CancellationCode': str}
df = pd.read_csv('airline_dec_2008_50k.csv', dtype=dtype, low_memory=False)

# Вывод списка всех колонок до преобразования
print("Колонки до преобразования:")
print(df.columns)

# Преобразование признаков времени в новые признаки
def convert_time_feature(df, feature_name):
    df[feature_name] = df[feature_name].astype(str).str.zfill(4)

    # Добавляем проверку наличия колонки перед преобразованием
    if feature_name in df.columns:
        df[f'{feature_name}_Hour'] = df[feature_name].apply(lambda x: np.nan if not x[:-2].isdigit() else float(x[:-2]))
        df[f'{feature_name}_Minute'] = df[feature_name].apply(lambda x: np.nan if not x[-2:].isdigit() else float(x[-2:]))
        df.drop([feature_name], axis=1, inplace=True)
    else:
        print(f"Колонка '{feature_name}' не найдена.")

time_features = ['DepTime', 'CRSDepTime', 'ArrTime', 'CRSArrTime']

for feature in time_features:
    convert_time_feature(df, feature)

# Вывод списка всех колонок после преобразования
print("Колонки после преобразования:")
print(df.columns)

# Печать уникальных значений временных признаков после преобразования
for feature in time_features:
    print(f"Unique values for {feature}: {df[feature].unique()}")

# Преобразование категориальных признаков в one-hot encoding
categorical_features = ['FlightNum', 'TailNum', 'ActualElapsedTime', 'CRSElapsedTime', 'AirTime', 'TaxiIn', 'TaxiOut']

df[categorical_features] = df[categorical_features].astype('category')
df = pd.get_dummies(df, columns=categorical_features, dummy_na=True)

df = pd.get_dummies(df, columns=['Origin', 'Dest'])

any_null_values_after_transform = df.isnull().any().any()
total_null_elements_after_transform = df.isnull().sum().sum()

# Проверка наличия пропущенных значений после преобразований
print(f"Имеются ли в данных пропущенные значения после преобразований?: {any_null_values_after_transform}")
print(f"Сколько всего пропущенных элементов в таблице 'объект-признак' после преобразований?: {total_null_elements_after_transform}")



df = extract_hour_minute(df, 'DepTime')
df = extract_hour_minute(df, 'CRSDepTime')
df = extract_hour_minute(df, 'ArrTime')
df = extract_hour_minute(df, 'CRSArrTime')

# Шаг 13: Исключение признаков
df = df.drop(['TailNum', 'Year'], axis=1)

# Шаг 13: Исключение сильно коррелирующих признаков
df = df.drop(['ArrDelay', 'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay'], axis=1)


# Шаг 15: Преобразование данных
def transform_data(data):
    # Замена пропущенных значений
    data = data.fillna({'CancellationCode': 'nan'})

    # Масштабирование вещественных признаков
    numeric_features = data.select_dtypes(include=['int64', 'float64']).columns
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('scaler', StandardScaler())
    ])

    # One-hot-кодирование категориальных признаков
    categorical_features = data.select_dtypes(include=['object']).columns
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='nan')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Объединение преобразованных признаков
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ])

    return preprocessor.fit_transform(data)


X = df.drop('DepDelay', axis=1)
y = df['DepDelay']

X_transformed = transform_data(X)
print(f'Количество признаков после преобразования: {X_transformed.shape[1]}')

# Шаг 16: Разбиение выборки
X_train, X_test, y_train, y_test = train_test_split(X_transformed, y, test_size=0.3, random_state=42)

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

#20

# возвращает вектор прогнозов линейной модели с вектором весов w для выборки X
def make_pred(X, w):
    return np.dot(X, w)

# возвращает значение функционала MSPE для выборки (X, y) и вектора весов w
def get_func(w, X, y):
    predictions = make_pred(X, w)
    errors = predictions - y
    return np.mean(errors**2)

# возвращает градиент функционала MSPE для выборки (X, y) и вектора весов w
def get_grad(w, X, y):
    predictions = make_pred(X, w)
    errors = predictions - y
    gradient = 2/len(y) * np.dot(X.T, errors)
    return gradient

# возвращает значение регуляризованного функционала MSPE для выборки (X, y) и вектора весов w
def get_reg_func(w, X, y, alpha):
    mse = get_func(w, X, y)
    reg_term = alpha * np.sum(w**2)
    return mse + reg_term

# возвращает градиент регуляризованного функционала MSPE для выборки (X, y) и вектора весов w
def get_reg_grad(w, X, y, alpha):
    mse_grad = get_grad(w, X, y)
    reg_grad = 2 * alpha * w
    return mse_grad + reg_grad

#21
def grad_descent(X, y, step_size, max_iter, eps, is_reg):
    w = np.zeros(X.shape[1])  # начальное значение весов
    func_values = []  # список значений функционала на каждой итерации

    for i in range(max_iter):
        grad = get_reg_grad(w, X, y, alpha) if is_reg else get_grad(w, X, y)
        w = w - step_size * grad  # обновление весов

        func_val = get_reg_func(w, X, y, alpha) if is_reg else get_func(w, X, y)
        func_values.append(func_val)

        # проверка условия останова
        if i > 0 and np.linalg.norm(w - prev_w) < eps:
            break

        prev_w = w.copy()

    return w, func_values

#22

import matplotlib.pyplot as plt

# данные
X_train, y_train = ...

# параметры
step_sizes = [0.001, 1, 10]
init_weights_modes = ['zeros', 'random']

# графики
plt.figure(figsize=(12, 8))

for step_size in step_sizes:
    for init_mode in init_weights_modes:
        w_init = np.zeros(X_train.shape[1]) if init_mode == 'zeros' else np.random.rand(X_train.shape[1])
        _, func_values = grad_descent(X_train, y_train, step_size, max_iter=100, eps=1e-6, is_reg=False)

        label = f'Step Size: {step_size}, Init Mode: {init_mode}'
        plt.plot(func_values, label=label)

plt.title('Convergence of Linear Regression with MSPE')
plt.xlabel('Iteration')
plt.ylabel('MSPE')
plt.legend()
plt.show()

#23
def sgd(X, y, step_size, max_iter, eps, is_reg):
    w = np.zeros(X.shape[1])  # начальное значение весов
    func_values = []  # список значений функционала на каждой итерации

    for i in range(max_iter):
        idx = np.random.randint(0, len(y))  # выбор случайного объекта
        grad = get_reg_grad(w, X[idx], y[idx], alpha) if is_reg else get_grad(w, X[idx], y[idx])
        w = w - step_size * grad  # обновление весов

        func_val = get_reg_func(w, X, y, alpha) if is_reg else get_func(w, X, y)
        func_values.append(func_val)

        # проверка условия останова
        if i > 0 and np.linalg.norm(w - prev_w) < eps:
            break

        prev_w = w.copy()

    return w, func_values

#24
# данные
X_train, y_train = ...

# графики
plt.figure(figsize=(12, 8))

_, func_values = sgd(X_train, y_train, step_size=0.01, max_iter=1000, eps=1e-6, is_reg=False)
plt.plot(func_values, label='MSPE (SGD)')

_, func_values_reg = sgd(X_train, y_train, step_size=0.01, max_iter=1000, eps=1e-6, is_reg=True)
plt.plot(func_values_reg, label='Regularized MSPE (SGD)')

plt.title('Convergence of Linear Regression with MSPE and Regularized MSPE (SGD)')
plt.xlabel('Iteration')
plt.ylabel('MSPE')
plt.legend()
plt.show()


#25
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# данные
X_test, y_test = ...

# обучение стандартной линейной регрессии
lr = LinearRegression()
lr.fit(X_train, y_train)

# прогнозы
y_pred = lr.predict(X_test)

# метрики
mspe_standard = get_func(lr.coef_, X_test, y_test)
mse_standard = mean_squared_error(y_test, y_pred)
r2_standard = r2_score(y_test, y_pred)

print(f'MSPE (Standard Linear Regression): {mspe_standard}')
print(f'MSE (Standard Linear Regression): {mse_standard}')
print(f'R^2 (Standard Linear Regression): {r2_standard}')




