import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import matplotlib.pyplot as plt

class GraphPlotter:
    def __init__(self, master):
        self.master = master
        self.master.title("График функции")

        self.create_widgets()
        self.initialize_variables()

    def create_widgets(self):
        self.func_entry = tk.Entry(self.master, width=40)
        self.func_entry.pack(pady=10)
        self.func_entry.insert(0, "x + 2 * np.sin(x) + np.cos(3 * x)")

        tk.Button(self.master, text="Построить график", command=self.plot_function).pack(pady=5)
        tk.Button(self.master, text="Загрузить данные", command=self.load_data).pack(pady=5)

        tk.Label(self.master, text="Масштаб OX:").pack()
        self.x_scale = tk.Scale(self.master, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL)
        self.x_scale.pack()

        tk.Label(self.master, text="Масштаб OY:").pack()
        self.y_scale = tk.Scale(self.master, from_=0.1, to=10, resolution=0.1, orient=tk.HORIZONTAL)
        self.y_scale.pack()

        tk.Label(self.master, text="Смещение по X:").pack()
        self.x_offset = tk.DoubleVar(value=0)
        tk.Entry(self.master, textvariable=self.x_offset).pack()

        tk.Label(self.master, text="Смещение по Y:").pack()
        self.y_offset = tk.DoubleVar(value=0)
        tk.Entry(self.master, textvariable=self.y_offset).pack()

    def initialize_variables(self):
        self.x_scale_var = tk.DoubleVar(value=1)
        self.y_scale_var = tk.DoubleVar(value=1)

    def plot_function(self):
        func_str = self.func_entry.get()
        try:
            func = eval("lambda x: " + func_str)
            x = np.linspace(-50, 50, 5000)
            y = func(x) * self.y_scale.get()
            x_scaled = (x + self.x_offset.get()) * self.x_scale.get()
            self.plot_graph(x_scaled, y, f"f(x) = {func_str}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось построить график: {e}")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
        if file_path:
            try:
                data = np.loadtxt(file_path, delimiter=',')
                if data.ndim == 2 and data.shape[1] == 2:
                    x, y = data[:, 0], data[:, 1]
                    self.plot_graph(x, y, "Загруженные данные")
                else:
                    messagebox.showerror("Ошибка", "Неверный формат файла.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

    def plot_graph(self, x, y, title):
        plt.figure(figsize=(10, 6))
        plt.plot(x, y, label=title)
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')
        plt.grid(color='gray', linestyle='--', linewidth=0.5)
        plt.title(title)
        plt.xlabel("X")
        plt.ylabel("f(X)")
        plt.legend()
        plt.xlim(-10, 10)
        plt.ylim(-10, 10)
        plt.show()

root = tk.Tk()
app = GraphPlotter(root)
root.mainloop()
