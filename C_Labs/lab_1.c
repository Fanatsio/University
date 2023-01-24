#include <stdio.h>

int main() {
    double a, b, x;
    double sum, res;
    printf("Enter a -> ");
    scanf("%lf", &a);
    printf("Enter b -> ");
    scanf("%lf", &b);
    printf("Enter x -> ");
    scanf("%lf", &x);
    sum = a + b;
    if (sum < x)
        res = sum / x;
    else if (sum == x)
        res = b / x;
    else
        res = x / sum;
    printf("result = %.3lf", res);
    return 0;
}