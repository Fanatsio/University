import pandas as pd

# Загрузка данных из CSV файла
data = pd.read_csv('airline_dec_2008_50k.csv', na_values=['NA'])

# Статистика по расстояниям
mean_distance = data['Distance'].mean()
min_distance = data['Distance'].min()
max_distance = data['Distance'].max()

print(f"Среднее расстояние: {mean_distance}")
print(f"Минимальное расстояние: {min_distance}")
print(f"Максимальное расстояние: {max_distance}")

# Поиск данных о минимальном расстоянии
min_distance_flight = data[data['Distance'] == min_distance]
print("\nДанные о рейсах с минимальным расстоянием:")
print(min_distance_flight[['FlightNum', 'DayOfWeek', 'Distance']])

# Поиск данных о том же рейсе в другие дни
same_flight_other_days = data[data['FlightNum'] == min_distance_flight['FlightNum'].iloc[0]]
print("\nДанные о том же рейсе в другие дни:")
print(same_flight_other_days[['FlightNum', 'DayOfWeek', 'Distance']])

# Аэропорт с наибольшим количеством вылетов
most_departures_airport = data['Origin'].value_counts().idxmax()

print(f"\nАэропорт с наибольшим количеством вылетов: {most_departures_airport}")

# Город, в котором находится аэропорт с наибольшим количеством вылетов
airport_city = data[data['Origin'] == most_departures_airport]['OriginCityName'].iloc[0]

print(f"Город аэропорта: {airport_city}")
