
---

### 1. Импорты
```python
import math
import tkinter as tk
from tkinter import messagebox
```
- `math`: Используется для вычисления таблицы констант `T` через функцию `sin`.
- `tkinter`: Библиотека для создания графического интерфейса.
- `messagebox`: Модуль для отображения всплывающих окон (например, предупреждений).

---

### 2. Функция `left_rotate`
```python
def left_rotate(value, shift):
    """Левый циклический сдвиг 32-битного числа."""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF
```
- **Что делает**: Выполняет циклический сдвиг влево для 32-битного числа.
- **Параметры**:
  - `value`: Число, которое нужно сдвинуть.
  - `shift`: Количество бит для сдвига.
- **Как работает**:
  - `value << shift`: Сдвигает биты влево.
  - `value >> (32 - shift)`: Сдвигает оставшиеся биты вправо.
  - `|` (или): Объединяет результаты.
  - `& 0xFFFFFFFF`: Ограничивает результат 32 битами (маска).
- **Пример**: Если `value = 0b1011` (11) и `shift = 2`, то результат будет `0b1100` (12) с учетом циклического сдвига.

---

### 3. Функция `md5`
```python
def md5(message):
    """Реализация MD5 хеширования."""
```
Это основная функция, которая вычисляет MD5-хеш. Разберем ее по шагам.

#### 3.1 Константы
```python
S = [
    [7, 12, 17, 22],  # Раунд 1
    [5, 9, 14, 20],   # Раунд 2
    [4, 11, 16, 23],  # Раунд 3
    [6, 10, 15, 21]   # Раунд 4
]
T = [int(2**32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
```
- `S`: Таблица сдвигов для каждого из 4 раундов (16 операций в каждом).
- `T`: Таблица из 64 чисел, вычисляемых как `2^32 * |sin(i+1)|`, где `i` — индекс от 0 до 63. Это фиксированные константы MD5.

#### 3.2 Инициализация буфера
```python
A, B, C, D = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
```
- Это начальные значения четырех 32-битных регистров (`A`, `B`, `C`, `D`), которые будут изменяться в процессе хеширования. Они определены в спецификации MD5.

#### 3.3 Дополнение сообщения
```python
original_byte_len = len(message)
original_bit_len = original_byte_len * 8
message += b'\x80'
message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
message += original_bit_len.to_bytes(8, byteorder='little')
```
- **Что делает**: Подготавливает входное сообщение к обработке.
- **Шаги**:
  1. `original_bit_len`: Длина сообщения в битах.
  2. `message += b'\x80'`: Добавляет бит "1" (в виде байта `0x80`).
  3. `b'\x00' * ...`: Дополняет сообщение нулями до длины, кратной 64 байтам, оставляя место для длины (56 байт в конце блока).
  4. `original_bit_len.to_bytes(8, 'little')`: Добавляет длину сообщения (8 байт) в little-endian формате.

#### 3.4 Обработка блоков
```python
for chunk_start in range(0, len(message), 64):
    chunk = message[chunk_start:chunk_start + 64]
    X = [int.from_bytes(chunk[j:j + 4], byteorder='little') for j in range(0, 64, 4)]
```
- **Что делает**: Разбивает сообщение на блоки по 64 байта.
- `X`: Преобразует каждый блок в массив из 16 чисел по 32 бита (4 байта).

#### 3.5 Основной цикл MD5
```python
a, b, c, d = A, B, C, D

for i in range(64):
    if i < 16:
        F = (b & c) | ((~b) & d)
        g = i
    elif i < 32:
        F = (d & b) | ((~d) & c)
        g = (5 * i + 1) % 16
    elif i < 48:
        F = b ^ c ^ d
        g = (3 * i + 5) % 16
    else:
        F = c ^ (b | (~d))
        g = (7 * i) % 16

    F = (F + a + X[g] + T[i]) & 0xFFFFFFFF
    shift = S[i // 16][i % 4]
    a, d, c, b = d, c, b, (b + left_rotate(F, shift)) & 0xFFFFFFFF
```
- **Что делает**: Выполняет 64 итерации, разделенные на 4 раунда (по 16 операций).
- **Раунды**:
  1. `i < 16`: Использует функцию `(b & c) | ((~b) & d)`.
  2. `i < 32`: Использует `(d & b) | ((~d) & c)`.
  3. `i < 48`: Использует `b ^ c ^ d`.
  4. `i >= 48`: Использует `c ^ (b | (~d))`.
- `g`: Индекс для выбора слова из блока `X`.
- `F = (F + a + X[g] + T[i]) & 0xFFFFFFFF`: Обновляет `F`, добавляя текущие значения.
- `shift`: Берет значение сдвига из таблицы `S`.
- `a, d, c, b = ...`: Обновляет регистры с учетом циклического сдвига.

#### 3.6 Обновление буфера
```python
A = (A + a) & 0xFFFFFFFF
B = (B + b) & 0xFFFFFFFF
C = (C + c) & 0xFFFFFFFF
D = (D + d) & 0xFFFFFFFF
```
- После обработки каждого блока добавляет промежуточные результаты к исходным значениям.

#### 3.7 Формирование результата
```python
return (A.to_bytes(4, byteorder='little') +
        B.to_bytes(4, byteorder='little') +
        C.to_bytes(4, byteorder='little') +
        D.to_bytes(4, byteorder='little')).hex()
```
- Объединяет `A`, `B`, `C`, `D` в 16-байтный результат (каждый по 4 байта) и преобразует в hex-строку.

---

### 4. Графический интерфейс
#### 4.1 `calculate_md5`
```python
def calculate_md5():
    text = entry.get()
    if not text:
        messagebox.showwarning("Ошибка", "Введите текст для хеширования")
        return
    md5_hash = md5(text.encode('utf-8'))
    result_entry.config(state='normal')
    result_entry.delete(0, tk.END)
    result_entry.insert(0, md5_hash)
    result_entry.config(state='readonly')
```
- Берет текст из поля ввода, кодирует его в байты (`utf-8`), вычисляет хеш и отображает результат.

#### 4.2 `copy_to_clipboard`
```python
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_entry.get())
    root.update()
    messagebox.showinfo("Копирование", "Хеш скопирован в буфер обмена")
```
- Копирует хеш в буфер обмена и показывает сообщение.

#### 4.3 Создание интерфейса
```python
root = tk.Tk()
root.title("MD5 Хеширование")
root.geometry("400x250")

tk.Label(root, text="Введите текст:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

tk.Button(root, text="Вычислить MD5", command=calculate_md5).pack(pady=10)

tk.Label(root, text="MD5 Хеш:").pack(pady=5)
result_entry = tk.Entry(root, width=50, state='readonly')
result_entry.pack(pady=5)

tk.Button(root, text="Копировать хеш", command=copy_to_clipboard).pack(pady=10)

root.mainloop()
```
- Создает окно с полем ввода, кнопкой для вычисления хеша, полем вывода и кнопкой копирования.

---

### Как работает алгоритм MD5 в целом
1. Принимает сообщение (байты).
2. Дополняет его до нужной длины.
3. Разбивает на 64-байтные блоки.
4. Обрабатывает каждый блок через 64 операции с использованием нелинейных функций, сдвигов и констант.
5. Возвращает 128-битный (16-байтный) хеш в виде hex-строки.

---