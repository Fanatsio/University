import numpy as np

n = int(input('Enter n: '))
m = int(input('Enter m: '))

f = lambda x: np.cos(1.7 ** (x + 1) - 2.7)
g = lambda x: 2 ** x + x ** 2 - 2

arr = np.empty((n, m))

res = -1e9

for i in range(n):
    for j in range(m):
        arr[i, j] = f(i + 1) + g(j + 1)

arr2 = np.sum(arr, axis=1)

print(round(np.max(arr2), 6))
