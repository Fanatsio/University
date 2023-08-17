#include <stdio.h>
#include <math.h>

int main() 
{
    double x;
    printf("Enter x { 6.42700 <= x <= 7.31100} -> ");
    scanf("%lf", &x);
    if (6.42700 <= x && x <= 7.31100)
    {
        double y = sqrt(sin(2*x)) + sqrt(sin(3*x));
        double z = sqrt(sqrt(log(tan(y - (M_PI / 8)))));
        printf("y(x) = %lf\nz(x) = %lf\n", y, z);
    }
    else
        printf("x value if incorrect !\n");
    return 0;
}