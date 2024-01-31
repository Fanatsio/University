#ifndef LAB1_ARKANOID_MATHHELPER_H
#define LAB1_ARKANOID_MATHHELPER_H

#define _USE_MATH_DEFINES
#include <math.h>

#include <limits>

namespace arkanoid {

    constexpr double pi = M_PI;

    constexpr double deg_0 = 0.0;
    constexpr double deg_15 = pi / 12.0;
    constexpr double deg_30 = 2 * deg_15;
    constexpr double deg_45 = pi / 4.0;
    constexpr double deg_60 = deg_45 + deg_15;
    constexpr double deg_75 = deg_60 + deg_15;
    constexpr double deg_90 = pi / 2.0;
    constexpr double deg_105 = deg_90 + deg_15;
    constexpr double deg_120 = deg_105 + deg_15;
    constexpr double deg_135 = deg_120 + deg_15;
    constexpr double deg_150 = deg_135 + deg_15;
    constexpr double deg_165 = deg_150 + deg_15;
    constexpr double deg_180 = pi;
    constexpr double deg_195 = deg_180 + deg_15;
    constexpr double deg_210 = deg_195 + deg_15;
    constexpr double deg_225 = deg_210 + deg_15;
    constexpr double deg_240 = deg_225 + deg_15;
    constexpr double deg_255 = deg_240 + deg_15;
    constexpr double deg_270 = 3 * deg_90;
    constexpr double deg_285 = deg_270 + deg_15;
    constexpr double deg_300 = deg_285 + deg_15;
    constexpr double deg_315 = deg_270 + deg_45;
    constexpr double deg_330 = deg_315 + deg_15;
    constexpr double deg_345 = deg_330 + deg_15;
    constexpr double deg_360 = 2 * pi;

    constexpr double degreesToRadient(double degree)
    {
        return degree * pi / 180.0;
    }

    constexpr double radientToDegrees(double radient)
    {
        return radient * 180.0 / pi;
    }
}  // namespace arkanoid

#endif //LAB1_ARKANOID_MATHHELPER_H
