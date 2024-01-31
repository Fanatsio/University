#ifndef LAB1_ARKANOID_GRID_H
#define LAB1_ARKANOID_GRID_H

#include <iosfwd>
#include <vector>

namespace arkanoid {

    class Ball;
    class Brick;
    class Platform;
    class Wall;
    class GameObject;

    enum class Field {
        ball,
        brick1Hits,
        brick2Hits,
        brick3Hits,
        brick4Hits,
        brick5Hits,
        brick6Hits,
        brick7Hits,
        brick8Hits,
        brick9Hits,
        empty,
        plattform,
        wall
    };

    class Grid
    {
    public:
        Grid(std::size_t width, std::size_t height);
        ~Grid() = default;

        void add(const Ball& ball);
        void add(const Brick& brick);
        void add(const Platform& plattform);
        void add(const Wall& wall);
    private:
        void add(const GameObject& gameObject, const Field& field);

        std::vector<std::vector<Field>> mFields;
        friend std::ostream& operator<<(std::ostream& os, const Grid& obj);
    };

    std::vector<std::vector<Field>> init(
            std::size_t width, std::size_t height);

    std::ostream& operator<<(std::ostream& os, const Grid& obj);
}  // namespace arkanoid

#endif //LAB1_ARKANOID_GRID_H
