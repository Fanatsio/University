import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer


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



