#include <stdio.h>
#include <math.h>

double f(int n)
{
    double b, h, x, y;
    double I = 0.0;
    for (double x = 1.0 / n; x <= 2*M_PI; x += 2.0 / n)
    {
        if (x <= M_PI / 2)
            y = pow(2, x) - 2 + x * x;
        else
            y = sqrt(b + x) * exp(-((b + x) * (b + x)));
        I += y;
    }
    I *= 2.0 / n;
    return I;
}

int main() 
{
    double e;
    printf("Введите точность >> ");
    scanf("%lf", &e);
    int n = 1;
    double In = f(n), I2n = f(2*n);
    while((fabs(I2n - In) / 3) >= e)
    {
        printf("%lf для n = %d \n", I2n, n*2);
        n *= 2;
        In = I2n;
        I2n = f(2*n);
    }
    printf("%lf \n", I2n);
    return 0;
}