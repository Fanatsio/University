import os
import Functions as Fun


int_columns = ['CAC', 'DAX', 'FTSE', 'SMI']

while True:
    item = Fun.menu()

    match item:
        case 0:
            exit()
        case 1:
            Fun.graph()
        case 2:
            Fun.correlation_matrix(int_columns)
        case 3:
            Fun.histograms_of_average_values(int_columns)
        case 4:
            Fun.histogram_of_variance(int_columns)
        case 5:
            Fun.histograms_of_absolute_values()
        case 6:
            Fun.histograms_of_difference_values()
        case 7:
            Fun.scatterplot_without_shift()
        case 8:
            Fun.scatterplot_with_shift()
        case 9:
            Fun.covariance_matrix()

    os.system('CLS')
