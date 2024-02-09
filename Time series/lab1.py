import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('EuStockMarkets.csv')

# x_values = df['rownames']
DAX_values = df['DAX']
SMI_values = df['SMI']
CAC_values = df['CAC']
FTSE_values = df['FTSE']

plt.plot(DAX_values, color='blue', label='DAX')
plt.plot(SMI_values, color='red', label='SMI')
plt.plot(CAC_values, color='green', label='CAC')
plt.plot(FTSE_values, color='orange', label='FTSE')

plt.legend()

plt.title('График')
plt.xlabel('количество дней')
plt.ylabel('данные')
plt.grid(True)  # Добавление сетки

int_columns = ['CAC', 'DAX', 'FTSE', 'SMI']

correlation_matrix = df[int_columns].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Корреляционная матрица')

means = df[int_columns].mean()
variances = df[int_columns].var()

# Построение гистограммы средних значений
plt.figure(figsize=(10, 5))
plt.bar(means.index, means.values, color='blue')
plt.xlabel('Столбцы')
plt.ylabel('Среднее значение')
plt.title('Средние значения столбцов')
plt.xticks(rotation=45)

# Построение гистограммы дисперсий
plt.figure(figsize=(10, 5))
plt.bar(variances.index, variances.values, color='red')
plt.xlabel('Столбцы')
plt.ylabel('Дисперсия')
plt.title('Дисперсии столбцов')
plt.xticks(rotation=45)



plt.show()