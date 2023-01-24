#include <stdio.h>

int ex(int x, int k)
{
    return k ? x * ex(x, k - 1) : 1;
}

int wh(int x, int k)
{
  int res = 1;
  for(int i = 1; i <= k; i++)
    res = x * res;
  return res;
}

int main() {
    int n, d;
    printf("Enter n -> ");
    scanf("%d", &n);
    printf("Enter d -> ");
    scanf("%d", &d);
    printf("exponentiation = %d\n", ex(n, d));
    printf("res = %d\n", wh(n, d));
    return 0;
}