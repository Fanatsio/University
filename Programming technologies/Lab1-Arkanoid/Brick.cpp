#include "Brick.h"

namespace arkanoid {

    Brick::Brick(Point topLeft,
                 double width, double height, std::size_t hitpoints)
            :GameObject(topLeft,
                        topLeft.x + width, topLeft.y + height,
                        width, height, 0, 0),
             mHitpoints(hitpoints),
             mStartHitpoints(hitpoints)
    {
    }

    std::size_t Brick::startHitpoints() const
    {
        return mStartHitpoints;
    }

    std::size_t Brick::hitpoints() const
    {
        return mHitpoints;
    }

    void Brick::decreaseHitpoints()
    {
        --mHitpoints;
    }

    bool Brick::isDestroyed() const
    {
        return mHitpoints == 0;
    }
}