import pandas as pd

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
