#include <pthread.h>
#include <stdio.h>
#include <math.h>

typedef struct {
    int start_index;
    int end_index;
    int n;
} thread_args;

double func_first(double i, double j, int n) {
    double y;
    double I = 0.0;
    for(double x = i / n; x <= j; x += 2.1 / n) {
        y = (pow(x, 2) - 2 * pow(x, 3)) * cos(pow(x, 2));
        I += y;
    }
    return I;
}

double func_second(double j, double k, int n) {
    double y;
    double I = 0.0;
    for(double x = j / n; x <= k; x += 2.1 / n) {
        y = exp(sin(2 * x));
        I += y;
    }
    return I;
}

double integral_calc(int start, int mid, int end, int n) {
    double i = start;
    double j = mid + 1;
    double k = end;
    
    double result = func_first(i, j, n) + func_second(j, k, n);

    return result;
}

void *calculate(void *arg) {
    thread_args *args = (thread_args *)arg;
    int start = args->start_index;
    int end = args->end_index;
    int n = args->n;
    int mid = 0;

    thread_args left_args = {start, mid, n};
    thread_args right_args = {mid, end, n};
    pthread_t left_thread, right_thread;

    pthread_create(&left_thread, NULL, calculate, &left_args);
    pthread_create(&right_thread, NULL, calculate, &right_args);
    pthread_join(left_thread, NULL);
    pthread_join(right_thread, NULL);

    printf("%lf", integral_calc(start, mid, end, n));

    return 0;
}

int main() {
    double e;
    printf("Enter precision >> ");
    scanf("%lf", &e);

    /*double In = integral_calc(start, mid, end, n);
    double I2n = integral_calc(start, mid, end, 2 * n);
    while ((fabs(I2n - In) / 3) >= e) {
        printf("%lf for n = %d \n", I2n, n * 2);
        n *= 2;
        In = I2n;
        I2n = integral_calc(start, mid, end, 2 * n);
    }
    printf("%lf \n", I2n);*/
    thread_args args = {-3.1415/2, 3.1415/2, 1};
    pthread_t calc_thread;
    pthread_create(&calc_thread, NULL, calculate, &args);
    pthread_join(calc_thread, NULL);
    return 0;
}