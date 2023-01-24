#include <stdio.h>
#include <math.h>

int main()
{
    double x, h, i;
    printf("Enter h -> ");
    scanf("%lf", &h);
    printf("x               f(x)\n");
    printf("--------------------\n");
    while (x <= 3)
    {
        if (0 <= x && x <= 1.5)
        {
            double y = pow(2, x) - 2 + pow(x, 2);
            printf("%lf             ", x);
            printf("%lf\n", y);
        }
        if (1.5 < x && x <= 3.0)
        {
            double z = sqrt(x) * exp(-pow(x, 2));
            printf("%lf             ", x);
            printf("%lf\n", z);
        }
        i++;
        x = h * i;
    }
    return 0;
}