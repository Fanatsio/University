#include <stdio.h>
#include <stdlib.h>
#include <math.h>

void fill(int m, int n, double *(array[n]))
{
  for (int i = 0; i < m; i++)
    for (int j = 0; j < n; j++)
    {
      int k = i + 1;
      int l = j + 1;
      array[i][j] = cos(pow(1.7, k + 1) - 2.7) + pow(2, l) + l * l - 2;
    }
}

double find_max(int m, int n, double *(array[n]))
{
  double res = 0;
  double sum;
  for (int i = 0; i < m; i++)
  {
    sum = 0;
    for (int j = 0; j < n; j++)
      sum += array[i][j];
    if (res < sum)
      res = sum;
  }
  return res;
}

int main()
{
  int n, m;
  printf("Enter count of rows: ");
  scanf("%d", &m);
  printf("Enter count of columns: ");
  scanf("%d", &n);
  double **array = (double **)malloc(sizeof(double *) * m);
  if (!array)
  {
    printf("Memory allocation error!\n");
    exit(EXIT_FAILURE);
  }
  for (int i = 0; i < m; i++)
    array[i] = (double *)malloc(n * sizeof(double));
  fill(m, n, array);
  double res = find_max(m, n, array);
  printf("%lf\n", res);
  return 0;
}
