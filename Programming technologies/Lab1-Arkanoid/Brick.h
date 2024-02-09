#ifndef LAB1_ARKANOID_BRICK_H
#define LAB1_ARKANOID_BRICK_H

#include "GameObject.h"

namespace arkanoid {

    class Brick : public GameObject
    {
    public:
        Brick(Point topLeft, double width, double height, std::size_t hitpoints);
        ~Brick() override = default;

        double velocity() const = delete;
        void setVelocity(double velocity) = delete;

        [[maybe_unused]] double angle() const = delete;

        [[maybe_unused]] void setAngle(double angle) = delete;

        [[maybe_unused]] void move(const Point& delta) = delete;

        std::size_t startHitpoints() const;
        std::size_t hitpoints() const;

        void decreaseHitpoints();
        bool isDestroyed() const;
    private:
        const std::size_t mStartHitpoints;
        std::size_t mHitpoints;
    };
}

#endif
