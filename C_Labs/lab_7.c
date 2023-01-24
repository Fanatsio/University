#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void fill(int n, int m, int a[n][m])
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j < m; j++)
            a[i][j] = rand() % 10;
}

void trans(int n, int m, int a[n][m], int b[m][n])
{
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            b[i][j] = a[j][i];
}

void mult(int n, int m, int a[n][m], int b[m][n], int c[n][n])
{
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
        {
            c[i][j] = 0;
            for(int k = 0; k < m; k++)
                c[i][j] += a[i][k] * b[k][j];
        }
}

int main() {
    srand(time(NULL));
    int n, m;
    printf("n -> ");
    scanf("%d", &n);
    printf("m -> ");
    scanf("%d", &m);
    int a[n][m], b[m][n], c[n][n];
    fill(n, m, a);
    trans(n, m, a, b);
    mult(n, m, a, b, c);
    printf("A: \n");
    for (int i = 0; i < n; i++, putchar('\n'))
        for (int j = 0; j < m; j++)
            printf("%6d ", a[i][j]);
    printf("B: \n");
    for (int i = 0; i < m; i++, putchar('\n'))
        for (int j = 0; j < n; j++)
            printf("%6d ", b[i][j]);
    printf("C: \n");
    for (int i = 0; i < n; i++, putchar('\n'))
        for (int j = 0; j < n; j++)
            printf("%7d ", c[i][j]);
    return 0;
}