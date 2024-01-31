#include "NearlyEqual.h"

#include <limits>
#include <cmath>

namespace arkanoid {

    bool nearlyEqual(double a, double b)
    {
        return std::nextafter(a, std::numeric_limits<double>::lowest()) <= b
               && std::nextafter(a, std::numeric_limits<double>::max()) >= b;
    }

    bool nearlyEqual(double a, double b, int factor)
    {
        double min_a = a - (a - std::nextafter(
                a, std::numeric_limits<double>::lowest())) * factor;
        double max_a = a + (
                                   std::nextafter(a, std::numeric_limits<double>::max()) - a) * factor;

        return min_a <= b && max_a >= b;
    }
} // namespace arkanoid