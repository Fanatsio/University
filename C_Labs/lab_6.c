#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fill(int n, int a[n])
{
    for (int i = 0; i < n; i++)
    {
        a[i] = rand() % 10;
        printf("%d ", a[i]);
    }
}

void rep(int n, int a[n], int b[n])
{
    long int sum = 0, pr = 1;
    for (int i = 0; i < n; i++)
        for (int j = i + 1; j < n; j++)
            if (a[i] == a[j])
            {
                printf("i = %d    j = %d\n", i, j);
                for (int k = i; k < j; k++)
                {
                    sum += a[k];
                    pr *= a[k];
                }
                sum -= a[j];
                pr /= a[j];
                printf("sum = %ld    pr = %ld\n", sum, pr);
                for (int k = 0; k < n; k++)
                {
                    if (k == i)
                        b[k] = sum;
                    else if (k == j)
                        b[k] = pr;
                    else
                        b[k] = a[k];
                    printf("%d  ", b[k]);
                }
            }
}

int main() 
{
    srand(time(NULL));
    int n;
    printf("n -> ");
    scanf("%d", &n);
    int a[n], b[n];
    fill(n, a);
    printf("\n");
    rep(n, a, b);
    return 0;
}