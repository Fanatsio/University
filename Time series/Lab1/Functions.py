import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('EuStockMarkets.csv')

DAX_values = df['DAX']
SMI_values = df['SMI']
CAC_values = df['CAC']
FTSE_values = df['FTSE']


def menu():
    print("Лабораторная работа №1 \n"
          "1 - Построить графики всех величин\n"
          "2 - Построить матрицу корреляции \n"
          "3 - Построить гистограмму абсолютных значений \n"
          "4 - Построить гистограмму дисперсии \n"
          "5 - Построить гистограмму абсолютных значений \n"
          "6 - Построить гистограмму разностей \n"
          "7 - Построить диаграмма рассеяния без временного смещения \n"
          "8 - Построить диаграмма рассеяния с временным смещением \n"
          "9 - Построить ковариационную матрицу \n"
          "0 - Выход")
    menu_item = int(input("Enter >> "))
    return menu_item


def graph():
    plt.plot(DAX_values, color='blue', label='DAX')
    plt.plot(SMI_values, color='red', label='SMI')
    plt.plot(CAC_values, color='green', label='CAC')
    plt.plot(FTSE_values, color='orange', label='FTSE')

    plt.legend()

    plt.title('График')
    plt.xlabel('количество дней')
    plt.ylabel('данные')
    plt.grid(True)

    plt.show()


def correlation_matrix(columns):
    matrix = df[columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Корреляционная матрица')

    plt.show()


def histograms_of_average_values(columns):
    means = df[columns].mean()

    plt.figure(figsize=(10, 5))
    plt.bar(means.index, means.values, color='blue')
    plt.xlabel('Столбцы')
    plt.ylabel('Среднее значение')
    plt.title('Средние значения столбцов')
    plt.xticks(rotation=45)

    plt.show()


def histogram_of_variance(columns):
    variances = df[columns].var()

    plt.figure(figsize=(10, 5))
    plt.bar(variances.index, variances.values, color='red')
    plt.xlabel('Столбцы')
    plt.ylabel('Дисперсия')
    plt.title('Дисперсии столбцов')
    plt.xticks(rotation=45)

    plt.show()


def histograms_of_absolute_values():
    plt.figure(figsize=(10, 6))
    plt.hist(DAX_values.abs(), bins=60, color='skyblue', edgecolor='black', alpha=0.7, label='DAX')
    plt.hist(SMI_values.abs(), bins=60, color='salmon', edgecolor='black', alpha=0.7, label='SMI')
    plt.hist(CAC_values.abs(), bins=60, color='green', edgecolor='black', alpha=0.7, label='CAC')
    plt.hist(FTSE_values.abs(), bins=60, color='purple', edgecolor='black', alpha=0.7, label='FTSE')
    plt.title('Гистограмма абсолютных значений')
    plt.xlabel('Абсолютное значение')
    plt.ylabel('Количество')
    plt.legend()
    plt.grid(True)

    plt.show()


def histograms_of_difference_values():
    plt.figure(figsize=(10, 6))
    plt.hist(DAX_values.diff().dropna(), bins=60, color='skyblue', edgecolor='black', alpha=0.7, label='DAX')
    plt.hist(SMI_values.diff().dropna(), bins=60, color='salmon', edgecolor='black', alpha=0.7, label='SMI')
    plt.hist(CAC_values.diff().dropna(), bins=60, color='green', edgecolor='black', alpha=0.7, label='CAC')
    plt.hist(FTSE_values.diff().dropna(), bins=60, color='purple', edgecolor='black', alpha=0.7, label='FTSE')
    plt.title('Гистограмма разностей')
    plt.xlabel('Разница')
    plt.ylabel('Количество')
    plt.legend()
    plt.grid(True)

    plt.show()


def scatterplot_without_shift():
    plt.figure(figsize=(8, 6))
    plt.scatter(DAX_values, SMI_values, color='skyblue', alpha=0.7)
    plt.title('Диаграмма рассеяния двух временных рядов DAX и SMI')
    plt.xlabel('DAX')
    plt.ylabel('SMI')
    plt.grid(True)

    plt.show()


def scatterplot_with_shift():
    lag_smi = SMI_values.shift(1)
    diff_smi = lag_smi.diff()
    diff_dax = DAX_values.diff()
    plt.figure(figsize=(8, 6))
    plt.scatter(diff_smi, diff_dax, color='skyblue', alpha=1)
    plt.title('Диаграмма разности между временными рядами SMI и DAX \n (со смещением SMI на один временной период '
              'вперед)')
    plt.xlabel('разность значений SMI с временным смещением')
    plt.ylabel('Разность значений DAX')
    plt.grid(True)

    plt.show()


def covariance_matrix():
    cov_matrix = np.cov(DAX_values, SMI_values)
    std_x = np.std(DAX_values)
    std_y = np.std(SMI_values)
    corr_matrix = cov_matrix/(std_x*std_y)

    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap='coolwarm', linewidths=0.5)
    plt.title('Ковариационная матрица')
    plt.xlabel('DAX                                                  SMI')
    plt.ylabel('SMI                                                DAX')

    plt.show()
