#include <math.h>
#include <stdio.h>

double f(int n) {
  double y;
  double I = 0.0;
  for (double x = 1.0 / n; x <= 3.1415 / 2; x += 2.112 / n) {
    if ((x >= -3.1415 / 2) && (x <= 0))
      y = (pow(x, 2) - 2 * pow(x, 3)) * cos(pow(x, 2));
    else
      y = exp(sin(2 * x));
    I += y;
  }
  I *= 2.0 / n;
  return I;
}

int main() {
  double e;
  printf("Enter precision >> ");
  scanf("%lf", &e);
  int n = 1;
  double In = f(n);
  double I2n = f(2 * n);
  while ((fabs(I2n - In) / 3) >= e) {
    printf("%lf for n = %d \n", I2n, n * 2);
    n *= 2;
    In = I2n;
    I2n = f(2 * n);
  }
  printf("%lf \n", I2n);
  return 0;
}
