#include "Grid.h"

#include "Ball.h"
#include "Brick.h"
#include "Platform.h"
#include "Wall.h"

#include <algorithm>
#include <cmath>
#include <iostream>

namespace arkanoid {

    Grid::Grid(std::size_t width, std::size_t height)
            : mFields{ init(width, height) }
    {
    }

    void Grid::add(const Ball& ball)
    {
        add(ball, Field::ball);
    }

    void Grid::add(const Brick& brick)
    {
        if (brick.isDestroyed()) {
            return;
        }

        auto brickType = static_cast<int>(Field::brick1Hits);
        brickType = brickType + brick.hitpoints() - 1;
        add(brick, static_cast<Field>(brickType));
    }

    void Grid::add(const Platform& plattform)
    {
        add(plattform, Field::plattform);
    }

    void Grid::add(const Wall& wall)
    {
        add(wall, Field::wall);
    }

    void Grid::add(const GameObject& gameObject, const Field& field)
    {
        auto x_begin =
                static_cast<std::size_t>(gameObject.topLeft().x);
        auto x_end =
                static_cast<std::size_t>(gameObject.bottomRight().x);

        auto y_begin =
                static_cast<std::size_t>(gameObject.topLeft().y);
        auto y_end =
                static_cast<std::size_t>(gameObject.bottomRight().y);

        for (auto y = y_begin; y < y_end; ++y) {
            for (auto x = x_begin; x < x_end; ++x) {
                mFields.at(y).at(x) = field;
            }
        }
    }

    std::vector<std::vector<Field>> init(std::size_t width, std::size_t height)
    {
        std::vector<Field> row(width, Field::empty);
        std::vector<std::vector<Field>> fields(height, row);
        return fields;
    }

    std::ostream& operator<<(std::ostream& os, const Grid& obj)
    {
        auto symbolWall = "# ";
        auto symbolBall = "O ";
        auto symbolBrick = "1 ";
        auto symbolPlattform = "= ";
        auto symbolEmpty = ". ";

        auto symbolBrick1Hit = "1 ";
        auto symbolBrick2Hit = "2 ";
        auto symbolBrick3Hit = "3 ";
        auto symbolBrick4Hit = "4 ";
        auto symbolBrick5Hit = "5 ";
        auto symbolBrick6Hit = "6 ";
        auto symbolBrick7Hit = "7 ";
        auto symbolBrick8Hit = "8 ";
        auto symbolBrick9Hit = "9 ";

        auto size_y = obj.mFields.size();
        auto size_x = obj.mFields.at(0).size();

        for (const auto& row : obj.mFields) {

            for (const auto& field : row) {

                switch (field) {
                    case Field::ball:
                        os << symbolBall;
                        break;
                    case Field::brick1Hits:
                        os << symbolBrick1Hit;
                        break;
                    case Field::brick2Hits:
                        os << symbolBrick2Hit;
                        break;
                    case Field::brick3Hits:
                        os << symbolBrick3Hit;
                        break;
                    case Field::brick4Hits:
                        os << symbolBrick4Hit;
                        break;
                    case Field::brick5Hits:
                        os << symbolBrick5Hit;
                        break;
                    case Field::brick6Hits:
                        os << symbolBrick6Hit;
                        break;
                    case Field::brick7Hits:
                        os << symbolBrick7Hit;
                        break;
                    case Field::brick8Hits:
                        os << symbolBrick8Hit;
                        break;
                    case Field::brick9Hits:
                        os << symbolBrick9Hit;
                        break;
                    case Field::empty:
                        os << symbolEmpty;
                        break;
                    case Field::plattform:
                        os << symbolPlattform;
                        break;
                    case Field::wall:
                        os << symbolWall;
                        break;
                }
            }
            os << '\n';
        }
        return os;
    }
}  // namespace arkanoid