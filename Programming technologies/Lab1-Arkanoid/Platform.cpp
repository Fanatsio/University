#include "Platform.h"

namespace arkanoid {

    Platform::Platform(
            Point topLeft, double maxPositioX, double length)
            : GameObject(
            topLeft, maxPositioX, topLeft.y + 1,
            length, 1, mStartVelocity, mStartAngle),
              mInitPosition{ topLeft }
    {
    }

    void Platform::setToInitPosition()
    {
        setTopLeft(mInitPosition);
    }
}  // namespace arkanoid