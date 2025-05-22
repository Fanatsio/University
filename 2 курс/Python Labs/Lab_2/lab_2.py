# Первый способ
min = 100
for a in range(1, 10):
    for b in range(2, 10):
        for c in range(3, 10):
            if a != b and a != c and b != c:
                d = round((a ** 3 + b ** 3 + c ** 3) ** (1/3), 1)
                s = str(d)
                if s[s.index('.') + 1] == "0":
                    if d < min:
                        min = d
                else:
                    continue
print("min_1 =", int(min))

# Второй способ
def min_d(a, b, c, min):
    d = round((a ** 3 + b ** 3 + c ** 3) ** (1/3), 1)
    s = str(d)
    if s[s.index('.') + 1] == "0":
        if d < min:
            min = d
    if (a <= 10):
        return min_d(a + 1, b + 1, c + 1, min)
    else:
        return min
result = min_d(1, 2, 3, 100)
print("min_2 =", int(result))