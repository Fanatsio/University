#include <stdio.h>
#include <math.h>
#include <pthread.h>

double f(double x) {
    if (x < 0) {
        return (pow(x, 2) - 2 * pow(x, 3)) * cos(pow(x, 2));
    }
    return exp(sin(2 * x));
}

typedef struct {
    double a;
    double b;
    double eps;
    double sum;
} IntegralParams;

void* calculate_integral(void* arg) {
    IntegralParams* params = (IntegralParams*)arg;
    double a = params->a;
    double b = params->b;
    double eps = params->eps;

    int n = 1;
    double h = (b - a) / n;
    double prev_sum;
    params->sum = 0.0;

    do {
        prev_sum = params->sum;
        params->sum = 0.0;

        for (int i = 0; i < n; i++) {
            double x = a + (i + 0.5) * h;
            double partial_sum = f(x) * h;
            params->sum += partial_sum;
        }

        n *= 2;
        h /= 2;
    } while (fabs(params->sum - prev_sum) > eps);

    return NULL;
}

int main() {
    double a = - 3.1415 / 2;
    double b = 3.1415 / 2;
    double eps;

    printf("Enter precision >> ");
    scanf("%lf", &eps);

    IntegralParams params;
    params.a = a;
    params.b = b;
    params.eps = eps;

    pthread_t thread;
    pthread_create(&thread, NULL, calculate_integral, (void*)&params);
    pthread_join(thread, NULL);

    double result = params.sum;

    printf("%lf\n", result);
    return 0;
}