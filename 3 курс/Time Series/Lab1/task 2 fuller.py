import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller

data = pd.read_csv('AirQualityUCI.csv', sep=';', dtype={'Date': str, 'Time': str}, na_values=['NA', 'NaN'])
data['DateTime'] = pd.to_datetime(data["Date"] + " " + data["Time"], format='%d/%m/%Y %H.%M.%S')

data_co = data
data_co_test = data
data_nmhc = data
data_nmhc_test = data
data_c6h6 = data
data_nox = data 
data_nox_test = data
data_no2 = data 
data_no2_test = data
data_o3_test = data
data_t = data
data_rh = data
data_ah = data



data_co['CO(GT)'] = data_co['CO(GT)'].str.replace(',', '.').astype(float)
data_co = data_co[data_co['CO(GT)'] != -200]

data_co_test = data_co_test[data_co_test['PT08.S1(CO)'] != -200]

data_nmhc = data_nmhc[data_nmhc['NMHC(GT)'] != -200]

data_nmhc_test = data_nmhc_test[data_nmhc_test['PT08.S2(NMHC)'] != -200]

data_c6h6['C6H6(GT)'] = data_c6h6['C6H6(GT)'].str.replace(',', '.').astype(float)
data_c6h6 = data_c6h6[data_c6h6['C6H6(GT)'] != -200]

data_nox = data_nox[data_nox['NOx(GT)'] != -200]

data_nox_test = data_nox_test[data_nox_test['PT08.S3(NOx)'] != -200]

data_no2 = data_no2[data_no2['NO2(GT)'] != -200]

data_no2_test = data_no2_test[data_no2_test['PT08.S4(NO2)'] != -200]

data_o3_test = data_o3_test[data_o3_test['PT08.S5(O3)'] != -200]

data_t['T'] = data_t['T'].str.replace(',', '.').astype(float)
data_t = data_t[data_t['T'] != -200]

data_rh['RH'] = data_rh['RH'].str.replace(',', '.').astype(float)
data_rh = data_rh[data_rh['RH'] != -200]

data_ah['AH'] = data_ah['AH'].str.replace(',', '.').astype(float)
data_ah = data_ah[data_ah['AH'] != -200]

list1 = [data_co['CO(GT)'], data_co_test['PT08.S1(CO)'], data_nmhc['NMHC(GT)'], data_nmhc_test['PT08.S2(NMHC)'],
         data_c6h6['C6H6(GT)'], data_nox['NOx(GT)'], data_nox_test['PT08.S3(NOx)'], data_no2['NO2(GT)'], data_no2_test['PT08.S4(NO2)'],
         data_o3_test['PT08.S5(O3)'], data_t['T'], data_rh['RH'], data_ah['AH']]

for i in list1:
    result = adfuller(i.dropna())
    print(f'{i}')
    print('ADF статистика:', result[0])
    print('p-value:', result[1])
    print('Критические значения:', result[4])

# result = adfuller(data['CO(GT)'].dropna())
# print('ADF статистика:', result[0])
# print('p-value:', result[1])
# print('Критические значения:', result[4])

