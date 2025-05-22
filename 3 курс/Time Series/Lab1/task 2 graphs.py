import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

# ЧТО ТУТ ТАКОЕ??? работаем с файлом AirQualityUCI. делаем свой тип из двух столбцов дата и время, показываем только каждое 
# сотое значение так как из-за огромного кол-ва значений шкала наслаивается сама на себя
# наверно лучше разделить графики и отображать pt_name в одном графике а все остальные значения в другом, менять просто отображение




data = pd.read_csv('AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])
# data['Date'] = data['Date'].astype(str)
# data['Time'] = data['Time'].astype(str)

data['CO(GT)'] = data['CO(GT)'].str.replace(',', '.').astype(float)

# Удаляем строки, содержащие значение -200 в столбце CO(GT)
data = data[data['CO(GT)'] != -200]

data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

result = adfuller(data['CO(GT)'].dropna())

# Вывод результатов теста Дики-Фуллера
print('ADF статистика:', result[0])
print('p-value:', result[1])
print('Критические значения:', result[4])

# data_sampled = data.iloc[:100]

# date_v = data_sampled['DateTime']
# co = data_sampled['CO(GT)']
# pt_co = data_sampled['PT08.S1(CO)']
# nmhc = data_sampled['NMHC(GT)']
# c6h6 = data_sampled['C6H6(GT)']
# pt_nmhc = data_sampled['PT08.S2(NMHC)']
# nox = data_sampled['NOx(GT)']
# pt_nox = data_sampled['PT08.S3(NOx)']
# no2 = data_sampled['NO2(GT)']
# pt_no2 = data_sampled['PT08.S4(NO2)']
# pt_o3 = data_sampled['PT08.S5(O3)']
# temp = data_sampled['T']
# rh = data_sampled['RH']
# ah = data_sampled['AH']

# plt.figure(figsize=(20, 10))
# plt.plot(date_v, co)
# plt.title('временной ряд')
# plt.xlabel('Дата и время')
# plt.ylabel('данные')
# plt.grid(True)
# plt.show()


