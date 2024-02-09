#ifndef LAB1_ARKANOID_BALL_H
#define LAB1_ARKANOID_BALL_H

#include "GameObject.h"
#include "MathHelper.h"

namespace arkanoid {

    class Ball : public GameObject
    {
    public:
        Ball(Point topLeft, double maxPositionX, double maxPositionY);
        ~Ball() override = default;

        [[nodiscard]] bool isActive() const;
        void activate();
        void deactivate();

        void move(double elapsedTimeInMS) override;

    private:
        const Point mInitPosition;
        bool mIsActive;

        static constexpr auto startAngle{ deg_135 };
        static constexpr auto startVelocity{ 9.0 };
        static constexpr auto gravityVelocity{ 2.5 };

        static constexpr auto width{ 1 };
        static constexpr auto height{ 1 };
    };
}

#endif
