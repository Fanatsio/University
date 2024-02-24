# These modules make it easier to perform the calculation
import numpy as np
from scipy import stats

# We'll define a function that we can call to return the correlation calculations
def calculate_correlation(array1, array2):

    # Calculate Pearson correlation coefficient and p-value
    correlation, p_value = stats.pearsonr(array1, array2)

    # Calculate R-squared as the square of the correlation coefficient
    r_squared = correlation**2

    return correlation, r_squared, p_value

# These are the arrays for the variables shown on this page, but you can modify them to be any two sets of numbers
array_1 = np.array([217,232,215,211,252,229,217,240,210,227,254,260,318,312,379,444,473,629,801,1147,1217,])
array_2 = np.array([0.55,0.96,2.64,2.25,2.37,1.93,4.77,2.57,6.81,9.07,8.79,12.8,19.94,15.63,32.81,37.9,58.6,73.26,93.75,163.5,167.55,])
array_1_name = "Popularity of the first name Stevie"
array_2_name = "Amazon.com's stock price (AMZN)"

# Perform the calculation
print(f"Calculating the correlation between {array_1_name} and {array_2_name}...")
correlation, r_squared, p_value = calculate_correlation(array_1, array_2)

# Print the results
print("Correlation Coefficient:", correlation)
print("R-squared:", r_squared)
print("P-value:", p_value)