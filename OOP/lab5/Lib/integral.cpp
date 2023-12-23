// integral.cpp
#include <cmath>

extern "C" {
    double integrate(double a, double b, int n) {
        double h = (b - a) / n;
        double integral = 0.0;

        for (int i = 0; i < n; i++) {
            double x1 = a + i * h;
            double x2 = a + (i + 1) * h;
            integral += (std::cos(x1) + std::cos(x2)) * h / 2;
        }

        return 2 * integral * (-1);
    }
}
