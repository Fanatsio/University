### 1. Импорт библиотек
```python
import tkinter as tk
from tkinter import messagebox
```
- `tkinter` — библиотека для создания графического интерфейса.
- `messagebox` — модуль для отображения всплывающих сообщений (ошибок, предупреждений).

### 2. Определение констант
```python
RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ASCII_PRINTABLE_START, ASCII_PRINTABLE_END = 32, 126
ASCII_PRINTABLE_SIZE = ASCII_PRINTABLE_END - ASCII_PRINTABLE_START + 1
RUSSIAN_ALPHABET_SIZE = len(RUSSIAN_ALPHABET)
```
- `RUSSIAN_ALPHABET` — строка с буквами русского алфавита (33 символа).
- `ASCII_PRINTABLE_START` и `ASCII_PRINTABLE_END` — диапазон печатных символов ASCII (от пробела до тильды).
- `ASCII_PRINTABLE_SIZE` — количество символов в этом диапазоне (95).
- `RUSSIAN_ALPHABET_SIZE` — длина русского алфавита (33).

### 3. Словари для быстрого доступа
```python
RUS_UPPER = {c: i for i, c in enumerate(RUSSIAN_ALPHABET)}
RUS_LOWER = {c.lower(): i for i, c in enumerate(RUSSIAN_ALPHABET)}
```
- `RUS_UPPER` — словарь, где ключ — заглавная буква, значение — её индекс в алфавите (например, `'А': 0`).
- `RUS_LOWER` — то же самое, но для строчных букв (например, `'а': 0`).

### 4. Функция сдвига символа
```python
def shift_char(char, shift):
    if char in RUS_UPPER:
        return RUSSIAN_ALPHABET[(RUS_UPPER[char] + shift) % RUSSIAN_ALPHABET_SIZE]
    elif char in RUS_LOWER:
        return RUSSIAN_ALPHABET[(RUS_LOWER[char] + shift) % RUSSIAN_ALPHABET_SIZE].lower()
    elif ASCII_PRINTABLE_START <= ord(char) <= ASCII_PRINTABLE_END:
        return chr(ASCII_PRINTABLE_START + (ord(char) - ASCII_PRINTABLE_START + shift) % ASCII_PRINTABLE_SIZE)
    return char
```
- Эта функция сдвигает символ на заданное количество позиций (`shift`).
- Если символ — заглавная русская буква, сдвиг происходит в пределах русского алфавита, результат — заглавная буква.
- Если символ — строчная русская буква, то же самое, но результат — строчная.
- Если символ — в диапазоне ASCII (32–126), сдвиг в пределах этого диапазона.
- `%` (оператор модуля) обеспечивает циклический сдвиг (например, после "Я" идёт "А").
- Если символ не попадает ни в один из диапазонов, возвращается без изменений.

### 5. Функция шифра Цезаря
```python
def caesar_cipher(text, shift):
    return ''.join(shift_char(char, shift) for char in text)
```
- Применяет `shift_char` к каждому символу текста и объединяет результат в строку.

### 6. Обработка текста
```python
def process_text(encrypting=True):
    text = entry_text.get("1.0", tk.END).strip() if encrypting else entry_result.get("1.0", tk.END).strip()
    shift_input = shift_var.get().strip()
    
    if not text:
        messagebox.showwarning("Предупреждение", "Поле текста не должно быть пустым!")
        return
    
    if not shift_input:
        messagebox.showwarning("Предупреждение", "Поле сдвига не должно быть пустым!")
        return
    
    try:
        shift = int(shift_input) * (-1 if not encrypting else 1)
    except ValueError:
        messagebox.showerror("Ошибка", "Сдвиг должен быть целым числом!")
        return
    
    result_text = caesar_cipher(text, shift)
    
    entry_result.delete("1.0", tk.END)
    entry_result.insert("1.0", result_text)
```
- `encrypting=True` — шифрование, `False` — дешифрование.
- Берёт текст из поля ввода (`entry_text`) для шифрования или из поля результата (`entry_result`) для дешифрования.
- Проверяет, что текст и сдвиг не пустые, иначе показывает предупреждение.
- Преобразует сдвиг в число. Для дешифрования умножает на `-1` (обратный сдвиг).
- Если сдвиг не число, показывает ошибку.
- Выполняет шифр/дешифр и вставляет результат в поле `entry_result`.

### 7. Вспомогательные функции для интерфейса
```python
def create_label(parent, text, row, column):
    tk.Label(parent, text=text).grid(row=row, column=column, sticky="w", padx=10, pady=5)

def create_text_widget(parent, height, width, row, columnspan):
    widget = tk.Text(parent, height=height, width=width)
    widget.grid(row=row, column=0, columnspan=columnspan, padx=10)
    return widget

def create_button(parent, text, command, row, column):
    tk.Button(parent, text=text, command=command).grid(row=row, column=column, padx=10, pady=5)
```
- Создают и размещают метки, текстовые поля и кнопки в сетке (`grid`).

### 8. Создание интерфейса
```python
root = tk.Tk()
root.title("Шифр Цезаря")
root.resizable(False, False)

create_label(root, "Введите текст:", 0, 0)
entry_text = create_text_widget(root, 4, 50, 1, 2)

create_label(root, "Введите сдвиг:", 2, 0)
shift_var = tk.StringVar()
entry_shift = tk.Entry(root, textvariable=shift_var)
entry_shift.grid(row=2, column=1, padx=10)

create_button(root, "Зашифровать", lambda: process_text(True), 3, 0)
create_button(root, "Расшифровать", lambda: process_text(False), 3, 1)

create_label(root, "Результат:", 4, 0)
entry_result = create_text_widget(root, 4, 50, 5, 2)

root.update_idletasks()
width = root.winfo_reqwidth() + 20
height = root.winfo_reqheight() + 20
root.geometry(f"{width}x{height}")

root.mainloop()
```
- Создаётся окно с заголовком "Шифр Цезаря".
- `root.resizable(False, False)` — окно нельзя растягивать.
- Элементы:
  - Поле ввода текста (4 строки, 50 символов).
  - Поле для ввода сдвига (число).
  - Кнопки "Зашифровать" и "Расшифровать".
  - Поле для вывода результата.
- `root.geometry` задаёт размер окна на основе содержимого.
- `root.mainloop()` запускает главный цикл программы.

### Как это работает
1. Пользователь вводит текст и сдвиг.
2. Нажимает "Зашифровать" — текст шифруется с заданным сдвигом.
3. Нажимает "Расшифровать" — текст из поля результата дешифруется (обратный сдвиг).
4. Результат отображается в нижнем поле.

### Пример
- Текст: "Привет, World!"
- Сдвиг: 3
- Шифрование: "Стйгжу, Zruog!"
- Дешифрование (сдвиг -3): возвращает "Привет, World!"