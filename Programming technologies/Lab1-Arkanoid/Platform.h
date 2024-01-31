#ifndef LAB1_ARKANOID_PLATFORM_H
#define LAB1_ARKANOID_PLATFORM_H

#include "GameObject.h"

namespace arkanoid {

    class Platform : public GameObject
    {
    public:
        Platform(Point topLeft, double maxPositioX, double length);
        ~Platform() override = default;

        void setToInitPosition();
    private:
        const Point mInitPosition;

        static constexpr auto mStartAngle{ 0 };
        static constexpr auto mStartVelocity{ 10.0 };
    };
}  // namespace arkanoid

#endif //LAB1_ARKANOID_PLATFORM_H
