#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int *memory(int m, int n) 
{
  int *a = (int *)malloc(100 * 100 * sizeof(int));
  if (!a)
  {
    printf("Memory allocation error!\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < n; i++)
    for (int j = 0; j < m; j++)
        a[i * m + j] = i * m + j + 1;
  return a;
}

void print(int m, int n, int ar[m][n])
{
  for (int i = 0; i < m; i++) 
  {
    for (int j = 0; j < n; j++) 
      printf("% 4d ", ar[i][j]);
    printf("\n");
  }
  printf("\n");
}

void fill(int m, int n, int A[m][n]) 
{
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            A[i][j] = rand() % 10;
}

void trans(int m, int n, int A[m][n], int B[n][m])
{
    for (int i = 0; i < m; i++)
        for (int j = 0; j < n; j++)
            B[i][j] = A[j][i];
}

void mult(int m, int n, int A[m][n], int B[n][m], int C[m][m])
{
    for (int i = 0; i < m; i++)
        for (int j = 0; j < m; j++)
        {
            C[i][j] = 0;
            for(int k = 0; k < n; k++)
                C[i][j] += A[i][k] * B[k][j];
        }
}

int main()
{
    srand(time(NULL));
    int m, n;
    printf("Количество строк -> ");
    scanf("%d", &m);
    printf("Количество столбцов -> ");
    scanf("%d", &n);
    
    int *A = memory(m, n);
    printf("A:\n");
    fill(m, n, A);
    print(m, n, A);
    
    int *B = memory(n, m);
    printf("B:\n");
    trans(m, n, A, B);
    print(n, m, B);
    
    int *C = memory(m, m);
    printf("C:\n");
    mult(m, n, A, B, C);
    print(m, m, C);
    
    free(A);
    free(B);
    //free(C);
    
    return 0;
}