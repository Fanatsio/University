import tkinter as tk
from tkinter import messagebox
import random

def mod_exp(base, exp, mod):
    """Быстрое возведение в степень по модулю (алгоритм быстрого возведения в степень)."""
    result = 1
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def mod_inverse(a, mod):
    """Нахождение обратного элемента по модулю с использованием встроенной функции pow()."""
    return pow(a, -1, mod)

def generate_keys():
    """Генерация параметров алгоритма DSA и ключей."""
    q = 23  # Малое простое число (используется для демонстрации)
    p = 47  # p = kq + 1, где k = 2
    g = 2   # Генератор, выбранный так, чтобы g < p
    x = random.randint(1, q - 1)  # Приватный ключ (секретный)
    y = mod_exp(g, x, p)  # Публичный ключ
    return p, q, g, x, y

def hash_message(message):
    """Генерация хэша сообщения с использованием встроенной hash() функции."""
    return abs(hash(message)) % 23  # Используем q=23

def sign_message(message, p, q, g, x):
    """Создание цифровой подписи (r, s) по DSA."""
    h = hash_message(message)  # Получаем хэш от сообщения
    while True:
        k = random.randint(1, q - 1)  # Генерируем случайное k
        r = mod_exp(g, k, p) % q  # r = (g^k mod p) mod q
        if r == 0:
            continue  # r не должен быть 0
        k_inv = mod_inverse(k, q)  # k^(-1) mod q
        s = (k_inv * (h + x * r)) % q  # s = (h + xr) * k^(-1) mod q
        if s != 0:
            break  # s не должен быть 0
    return r, s

def verify_signature(message, r, s, p, q, g, y):
    """Проверка цифровой подписи (r, s)."""
    if not (0 < r < q and 0 < s < q):
        return False  # r и s должны быть в диапазоне (0, q)
    h = hash_message(message)
    w = mod_inverse(s, q)  # Вычисляем w = s^(-1) mod q
    u1 = (h * w) % q  # u1 = (h * w) mod q
    u2 = (r * w) % q  # u2 = (r * w) mod q
    v = ((mod_exp(g, u1, p) * mod_exp(y, u2, p)) % p) % q  # v = ((g^u1 * y^u2) mod p) mod q
    return v == r  # Подпись верна, если v == r

def generate_and_display_keys():
    global p, q, g, x, y
    p, q, g, x, y = generate_keys()
    key_entry.config(state='normal')
    key_entry.delete(1.0, tk.END)
    key_entry.insert(tk.END, f"p={p}\nq={q}\ng={g}\nx={x}\ny={y}")
    key_entry.config(state='disabled')

def sign():
    message = input_text.get()
    if not message:
        messagebox.showwarning("Ошибка", "Введите текст для подписи")
        return
    r, s = sign_message(message, p, q, g, x)
    result_label.config(text="Подпись:")
    result_text.config(state='normal')
    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, f"r={r}\ns={s}")
    result_text.config(state='disabled')

def verify():
    message = input_text.get()
    signature = result_text.get(1.0, tk.END).strip()
    r, s = map(int, signature.replace("r=", "").replace("s=", "").split("\n"))
    valid = verify_signature(message, r, s, p, q, g, y)
    messagebox.showinfo("Результат", "Подпись верна" if valid else "Подпись неверна")

root = tk.Tk()
root.title("DSA Подпись")
root.geometry("400x400")

tk.Label(root, text="Текст для подписи:").pack()
input_text = tk.Entry(root, width=50)
input_text.pack()

tk.Label(root, text="Ключи:").pack()
key_entry = tk.Text(root, width=50, height=5, state='disabled')
key_entry.pack()

tk.Button(root, text="Генерировать ключи", command=generate_and_display_keys).pack()
tk.Button(root, text="Подписать", command=sign).pack()
tk.Button(root, text="Проверить подпись", command=verify).pack()

result_label = tk.Label(root, text="Подпись:")
result_label.pack()

result_text = tk.Text(root, width=50, height=3, state='disabled')
result_text.pack()

root.mainloop()