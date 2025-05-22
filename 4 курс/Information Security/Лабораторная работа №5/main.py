import math
import tkinter as tk
from tkinter import messagebox

def left_rotate(value, shift):
    """Левый циклический сдвиг 32-битного числа."""
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

def md5(message):
    """Реализация MD5 хеширования."""
    # Константы
    S = [
        [7, 12, 17, 22],  # Раунд 1
        [5, 9, 14, 20],   # Раунд 2
        [4, 11, 16, 23],  # Раунд 3
        [6, 10, 15, 21]   # Раунд 4
    ]
    T = [int(2**32 * abs(math.sin(i + 1))) & 0xFFFFFFFF for i in range(64)]
    
    # Инициализация буфера
    A, B, C, D = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476
    
    # Дополнение сообщения
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8
    message += b'\x80'
    message += b'\x00' * ((56 - (original_byte_len + 1) % 64) % 64)
    message += original_bit_len.to_bytes(8, byteorder='little')

    # Обработка блоков
    for chunk_start in range(0, len(message), 64):
        chunk = message[chunk_start:chunk_start + 64]
        X = [int.from_bytes(chunk[j:j + 4], byteorder='little') for j in range(0, 64, 4)]

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

        A = (A + a) & 0xFFFFFFFF
        B = (B + b) & 0xFFFFFFFF
        C = (C + c) & 0xFFFFFFFF
        D = (D + d) & 0xFFFFFFFF

    return (A.to_bytes(4, byteorder='little') +
            B.to_bytes(4, byteorder='little') +
            C.to_bytes(4, byteorder='little') +
            D.to_bytes(4, byteorder='little')).hex()

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

def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(result_entry.get())
    root.update()
    messagebox.showinfo("Копирование", "Хеш скопирован в буфер обмена")

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