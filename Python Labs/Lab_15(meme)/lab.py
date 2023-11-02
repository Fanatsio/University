from math import sqrt, cos
from time import time

t = time()
n = int(input('Enter n: '))
m = int(input('Enter m: '))

f = lambda x: cos(1.7 ** (x + 1) - 2.7)
g = lambda x: 2 ** x + x ** 2 - 2

res = -1e9

for i in range(n):
    sum = 0
    for j in range(m):
        sum += f(i + 1) + g(j + 1)
    if sum > res:
        res = sum

print(round(res, 6))
end = time() - t
print(end, 'мс')
