import pandas as pd
import numpy as np
import timeit

df = pd.read_csv('city_temperature.csv')

int16_temperature = df['AvgTemperature'].astype(np.int16)
float64_temperature = df['AvgTemperature'].astype(np.float64)

start_time = timeit.default_timer()
result_int16 = np.sum(int16_temperature)
end_time = timeit.default_timer()
print(f"Время выполнения операции на массиве int16: {end_time - start_time} секунд")

start_time = timeit.default_timer()
result_float64 = np.sum(float64_temperature)
end_time = timeit.default_timer()
print(f"Время выполнения операции на массиве float64: {end_time - start_time} секунд")
