import tkinter as tk
from tkinter import messagebox

RUSSIAN_ALPHABET = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
ASCII_PRINTABLE_START, ASCII_PRINTABLE_END = 32, 126
ASCII_PRINTABLE_SIZE = ASCII_PRINTABLE_END - ASCII_PRINTABLE_START + 1
RUSSIAN_ALPHABET_SIZE = len(RUSSIAN_ALPHABET)

# Словари для быстрого доступа к индексам символов
RUS_UPPER = {c: i for i, c in enumerate(RUSSIAN_ALPHABET)}
RUS_LOWER = {c.lower(): i for i, c in enumerate(RUSSIAN_ALPHABET)}

def shift_char(char, shift):
    """Сдвиг символа на заданное значение в зависимости от алфавита."""
    if char in RUS_UPPER:
        return RUSSIAN_ALPHABET[(RUS_UPPER[char] + shift) % RUSSIAN_ALPHABET_SIZE]
    elif char in RUS_LOWER:
        return RUSSIAN_ALPHABET[(RUS_LOWER[char] + shift) % RUSSIAN_ALPHABET_SIZE].lower()
    elif ASCII_PRINTABLE_START <= ord(char) <= ASCII_PRINTABLE_END:
        return chr(ASCII_PRINTABLE_START + (ord(char) - ASCII_PRINTABLE_START + shift) % ASCII_PRINTABLE_SIZE)
    return char

def caesar_cipher(text, shift):
    """Применение шифра Цезаря к тексту."""
    return ''.join(shift_char(char, shift) for char in text)

def process_text(encrypting=True):
    """Обработка ввода, шифрование/дешифрование и вывод результата."""
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

def create_label(parent, text, row, column):
    tk.Label(parent, text=text).grid(row=row, column=column, sticky="w", padx=10, pady=5)

def create_text_widget(parent, height, width, row, columnspan):
    widget = tk.Text(parent, height=height, width=width)
    widget.grid(row=row, column=0, columnspan=columnspan, padx=10)
    return widget

def create_button(parent, text, command, row, column):
    tk.Button(parent, text=text, command=command).grid(row=row, column=column, padx=10, pady=5)

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