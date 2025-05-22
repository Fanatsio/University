import numpy as np
import pandas as pd

num_points = 500
x_values = np.linspace(0, 50, num_points)
f_values = np.sin(x_values) + 0.5 * x_values

data = pd.DataFrame({
    "x": x_values,
    "f(x)": f_values
})

file_path = "./Lab1/tabulated_function.csv"
data.to_csv(file_path, index=False)
