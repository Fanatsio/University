#include <pthread.h>
#include <stdio.h>
#include <math.h>

typedef struct {
    int start_index;
    int end_index;
} thread_args;

double func_first(int n) {
    
}

double integral_calc(int start, int mid, int end) {
    /*double y;
    double I = 0.0;
    for (double x = 1.0 / n; x <= 3.1415 / 2; x += 2.1 / n) {
        if ((x >= -3.1415 / 2) && (x <= 0))
        y = (pow(x, 2) - 2 * pow(x, 3)) * cos(pow(x, 2));
        else
        y = exp(sin(2 * x));
        I += y;
    }
    I *= 2.0 / n;
    return I;*/
    double i = start;
    double j = mid + 1;
    double k = start;
    for(double x = start; x <= end; x += 2.1) {

    }
}

void *calculate(void *arg) {
    thread_args *args = (thread_args *)arg;
    int start = args->start_index;
    int end = args->end_index;
    if (start < end) {
        int mid = 0;
        thread_args left_args = {start, mid};
        thread_args right_args = {mid, end};
        pthread_t left_thread, right_thread;
        pthread_create(&left_thread, NULL, calculate, &left_args);
        pthread_create(&right_thread, NULL, calculate, &right_args);
        pthread_join(left_thread, NULL);
        pthread_join(right_thread, NULL);
        integral_calc(start, mid, end);
    }
    return 0;
}

int main() {
    double e;
    printf("Enter precision >> ");
    scanf("%lf", &e);
    int n = 1;
    thread_args args = {-3.1415/2, 3.1415/2};
    pthread_t calc_thread;
    pthread_create(&calc_thread, NULL, calculate, &args);
    pthread_join(calc_thread, NULL);
    double In = f(n);
    double I2n = f(2 * n);
    while ((fabs(I2n - In) / 3) >= e) {
        printf("%lf for n = %d \n", I2n, n * 2);
        n *= 2;
        In = I2n;
        I2n = f(2 * n);
    }
    printf("%lf \n", I2n);
    return 0;
}