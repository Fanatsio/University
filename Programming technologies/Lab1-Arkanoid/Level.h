#ifndef LAB1_ARKANOID_LEVEL_H
#define LAB1_ARKANOID_LEVEL_H

#include "Ball.h"
#include "Brick.h"
#include "Platform.h"
#include "Wall.h"

#include <vector>

namespace arkanoid {

    class Wall;
    class Brick;
    class Platform;

    class Level
    {
    public:
        Level(long long score, int lives, int level, std::vector<Brick> bricks);
        ~Level() = default;

        void run();

        long long score() const;
        int lives() const;

        bool isGameOver() const;
    private:
        void handleBallMovementsAndCollisions(double elapsedTimeInMS);
        void printToConsole();

        Platform makePlatform();
        Ball makeBall();

        static constexpr int boardWidth{ 26 };
        static constexpr int boardHeight{ 18 };

        static constexpr auto plattformWidth{ 5.0 };
        static constexpr auto wallThickness{ 1.0 };

        static constexpr auto pointsPerBrick{ 100 };

        long long mScore;
        int mLives;
        const int mLevel;

        std::vector<Brick> mBricks;

        const Wall mLeftWall;
        const Wall mRightWall;
        const Wall mTopWall;

        Platform mPlatform;
        Ball mBall;

        bool mIsGameOver;
    };

    void movePlatformBetweenWalls(
            Platform& platform, const Wall& leftWall, const Wall& rightWall,
            double elapsedTimeInMS);

    Point calculatePlattformInitPosition(
            double plattformSize, double boardWidth, double boardHeight);

    Point calculateBallInitPosition(double boardWidth, double boardHeight);

    bool allBricksAreDestroyed(const std::vector<Brick>& bricks);

    std::vector<Brick> makeBricksLevel1();

    std::vector<Brick> makeBricksLevel2();
}  // namespace arkanoid

#endif //LAB1_ARKANOID_LEVEL_H
