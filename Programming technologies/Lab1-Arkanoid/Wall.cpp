#include "Wall.h"

namespace arkanoid {

    Wall::Wall(Point topLeft, double width, double height)
            :GameObject(topLeft,
                        topLeft.x + width, topLeft.y + height,
                        width, height, 0, 0)
    {
    }

}