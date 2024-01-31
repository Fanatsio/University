#include "Ball.h"

#include <algorithm>

namespace arkanoid {

    Ball::Ball(Point topLeft, double maxPositionX, double maxPositionY)
            :GameObject(topLeft,
                        maxPositionX, maxPositionY, width, height, 0.0, 0.0),
             mInitPosition{ topLeft },
             mIsActive{false}
    {
    }

    bool Ball::isActive()
    {
        return mIsActive;
    }

    void Ball::deactivate()
    {
        mIsActive = false;
        setAngle(0.0);
        setVelocity(0.0);
        setTopLeft(mInitPosition);
    }

    void Ball::activate()
    {
        mIsActive = true;
        setAngle(startAngle);
        setVelocity(startVelocity);
    }

    void Ball::move(double elapsedTimeInMS)
    {
        auto distanceY = calcTraveldWay(elapsedTimeInMS, gravityVelocity);

        auto p = topLeft();
        p.y += distanceY;
        setTopLeft(p);

        GameObject::move(elapsedTimeInMS);
    }

}  // namespace arkanoid