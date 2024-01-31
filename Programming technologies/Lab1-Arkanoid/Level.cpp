#include "Level.h"

#include "Console.h"
#include "Grid.h"
#include "Time.h"

#include <algorithm>
#include <iomanip>
#include <iostream>

namespace arkanoid {

    Level::Level(long long score, int lives, int level,
                 const std::vector<Brick> bricks)
            : mScore{score}, mLives{lives}, mLevel{level},
              mBricks{bricks},
              mLeftWall{
                      Point{0,0},
                      wallThickness, boardHeight
              },
              mRightWall{
                      Point{boardWidth - wallThickness, 0},
                      wallThickness, boardHeight
              },
              mTopWall{
                      Point{wallThickness, 0},
                      boardWidth - 2.0 * wallThickness, wallThickness
              },
              mPlatform{makePlatform()},
              mBall{makeBall()},
              mIsGameOver{false}
    {
    }

    void Level::run()
    {
        std::chrono::time_point<std::chrono::high_resolution_clock> t1;
        std::chrono::time_point<std::chrono::high_resolution_clock> t2;
        double elapsedTimeInMS{ 0.0 };

        for (;;) {
            t1 = getCurrentTime();

            if (!mBall.isActive() && console::spaceKeyHoldDown()) {
                mBall.activate();
            }

            movePlatformBetweenWalls(
                    mPlatform, mLeftWall, mRightWall, elapsedTimeInMS);

            if (mBall.isActive()) {
                handleBallMovementsAndCollisions(elapsedTimeInMS);
            }

            if (allBricksAreDestroyed(mBricks)) {
                return;
            }

            if (mIsGameOver) {
                return;
            }

            printToConsole();

            t2 = getCurrentTime();
            elapsedTimeInMS = arkanoid::getElapsedTime(t1, t2);
        }
    }

    long long Level::score() const
    {
        return mScore;
    }

    int Level::lives() const
    {
        return mLives;
    }

    bool Level::isGameOver() const
    {
        return mIsGameOver;
    }

    void Level::handleBallMovementsAndCollisions(double elapsedTimeInMS)
    {
        if (mBall.reflectIfHit(mRightWall)) {
            ;
        }
        else if (mBall.reflectIfHit(mLeftWall)) {
            ;
        }
        else if (mBall.reflectIfHit(mTopWall)) {
            ;
        }
        else if (mBall.reflectIfHit(mPlatform)) {
            ;
        }
        else if (mBall.bottomRight().y >= boardHeight) {

            wait(std::chrono::milliseconds{ 1000 });

            --mLives;
            if (mLives == 0) {
                mIsGameOver = true;
            }
            mBall.deactivate();
            mPlatform.setToInitPosition();
            return;
        }

        for (auto& brick : mBricks) {
            if (brick.isDestroyed()) {
                continue;
            }
            if (mBall.reflectIfHit(brick)) {
                brick.decreaseHitpoints();

                if (brick.isDestroyed()) {
                    mScore +=
                            pointsPerBrick * brick.startHitpoints();
                }
                break;
            }
        }

        mBall.move(elapsedTimeInMS);
    }

    void Level::printToConsole()
    {
        console::putCursorToStartOfConsole();

        Grid grid(
                static_cast<int>(boardWidth),
                static_cast<int>(boardHeight)
        );

        grid.add(mBall);
        grid.add(mPlatform);
        grid.add(mLeftWall);
        grid.add(mRightWall);
        grid.add(mTopWall);

        for (const auto& brick : mBricks) {
            grid.add(brick);
        }

        console::putCursorToStartOfConsole();
        std::cout << "Score:" << std::setw(15) << mScore << "     "
                  << "Lives:" << std::setw(4) << mLives << "     "
                  << "Level:" << std::setw(4) << mLevel << '\n'
                  << grid << '\n';

        //std::cout << std::setw(5) << mBall.topLeft().x << "   "
        //  << std::setw(5) << mBall.topLeft().y << "     "
        //  << std::setw(10) << radientToDegrees(mBall.angle())
        //  << std::setw(10) << radientToDegrees(mBall.quadrantAngle())
        //  << std::setw(3) << static_cast<int>(mBall.quadrant()) + 1 << '\n';

        //std::cout << std::setw(5) << mPlatform.topLeft().x << "   "
        //  << std::setw(5) << mPlatform.topLeft().y << "     "
        //  << std::setw(10) << radientToDegrees(mPlatform.angle())
        //  << std::setw(10) << radientToDegrees(mPlatform.quadrantAngle())
        //  << std::setw(3) << static_cast<int>(mPlatform.quadrant()) + 1 << '\n';
    }

    Platform Level::makePlatform()
    {
        return Platform{
                calculatePlattformInitPosition(
                        plattformWidth, boardWidth, boardHeight),
                static_cast<double>(boardWidth),
                plattformWidth,
        };
    }

    Ball Level::makeBall()
    {
        return Ball{ calculateBallInitPosition(boardWidth, boardHeight),
                     static_cast<double>(boardWidth),
                     static_cast<double>(boardHeight)
        };
    }

    void movePlatformBetweenWalls(
            Platform& platform, const Wall& leftWall, const Wall& rightWall,
            double elapsedTimeInMS)
    {
        if (console::rightKeyHoldDown()) {

            platform.setAngle(0.0);
            platform.move(elapsedTimeInMS);
        }
        else if (console::leftKeyHoldDown()) {

            platform.setAngle(deg_180);
            platform.move(elapsedTimeInMS);
        }

        if (platform.reflectIfHit(rightWall)) {
            ;
        }
        else if (platform.reflectIfHit(leftWall)) {
            ;
        }
    }

    Point calculatePlattformInitPosition(
            double plattformSize, double boardWidth, double boardHeight)
    {
        return Point{
                boardWidth / 2.0 - plattformSize / 2.0,
                boardHeight - 3.0
        };
    }

    Point calculateBallInitPosition(double boardWidth, double boardHeight)
    {
        return Point{
                boardWidth / 2.0 - 1,
                boardHeight - 4.0
        };
    }

    bool allBricksAreDestroyed(const std::vector<Brick>& bricks)
    {
        return std::find_if(bricks.begin(), bricks.end(),
                            [](const Brick& b)
                            {
                                return !b.isDestroyed();
                            }) == bricks.end();
    }

    std::vector<Brick> makeBricksLevel1()
    {
        constexpr auto brickLength = 3.0;
        constexpr auto brickHeight = 1.0;

        return std::vector<Brick>
                {
                        Brick{ Point{4,2},brickLength,brickHeight,1 },
                        Brick{ Point{7,2},brickLength,brickHeight,1 },
                        Brick{ Point{10,2},brickLength,brickHeight,1 },
                        Brick{ Point{13,2},brickLength,brickHeight,1 },
                        Brick{ Point{16,2},brickLength,brickHeight,1 },
                        Brick{ Point{19,2},brickLength,brickHeight,1 },

                        Brick{ Point{4,3},brickLength,brickHeight,1 },
                        Brick{ Point{19,3},brickLength,brickHeight,1 },

                        Brick{ Point{4,4},brickLength,brickHeight,1 },
                        Brick{ Point{10,4},brickLength,brickHeight,2 },
                        Brick{ Point{13,4},brickLength,brickHeight,2 },
                        Brick{ Point{19,4},brickLength,brickHeight,1 },

                        Brick{ Point{4,5},brickLength,brickHeight,1 },
                        Brick{ Point{19,5},brickLength,brickHeight,1 },

                        Brick{ Point{4,6},brickLength,brickHeight,1 },
                        Brick{ Point{7,6},brickLength,brickHeight,1 },
                        Brick{ Point{10,6},brickLength,brickHeight,1 },
                        Brick{ Point{13,6},brickLength,brickHeight,1 },
                        Brick{ Point{16,6},brickLength,brickHeight,1 },
                        Brick{ Point{19,6},brickLength,brickHeight,1 },
                };
    }

    std::vector<Brick> makeBricksLevel2()
    {
        constexpr auto brickLength = 3.0;
        constexpr auto brickHeight = 1.0;

        return std::vector<Brick>
                {
                        // draw a C
                        Brick{ Point{4,2},brickLength,brickHeight,1 },
                        Brick{ Point{7,2},brickLength,brickHeight,1 },
                        Brick{ Point{10,2},brickLength,brickHeight,1 },
                        Brick{ Point{13,2},brickLength,brickHeight,1 },
                        Brick{ Point{4,3},brickLength,brickHeight,1 },
                        Brick{ Point{4,4},brickLength,brickHeight,1 },
                        Brick{ Point{4,5},brickLength,brickHeight,1 },
                        Brick{ Point{4,6},brickLength,brickHeight,1 },
                        Brick{ Point{4,7},brickLength,brickHeight,1 },
                        Brick{ Point{4,8},brickLength,brickHeight,1 },
                        Brick{ Point{4,9},brickLength,brickHeight,1 },
                        Brick{ Point{4,10},brickLength,brickHeight,1 },
                        Brick{ Point{7,10},brickLength,brickHeight,1 },
                        Brick{ Point{10,10},brickLength,brickHeight,1 },
                        Brick{ Point{13,10},brickLength,brickHeight,1 },

                        // draw first +
                        Brick{ Point{13,6},brickHeight,brickHeight,2 },
                        Brick{ Point{14,6},brickHeight,brickHeight,3 },
                        Brick{ Point{15,4},brickHeight,brickHeight,2 },
                        Brick{ Point{15,5},brickHeight,brickHeight,3 },
                        Brick{ Point{15,6},brickHeight,brickHeight,4 },
                        Brick{ Point{15,7},brickHeight,brickHeight,3 },
                        Brick{ Point{15,8},brickHeight,brickHeight,2 },
                        Brick{ Point{16,6},brickHeight,brickHeight,3 },
                        Brick{ Point{17,6},brickHeight,brickHeight,2 },

                        // draw second +
                        Brick{ Point{19,6},brickHeight,brickHeight,5 },
                        Brick{ Point{20,6},brickHeight,brickHeight,6 },
                        Brick{ Point{21,4},brickHeight,brickHeight,5 },
                        Brick{ Point{21,5},brickHeight,brickHeight,3 },
                        Brick{ Point{21,6},brickHeight,brickHeight,7 },
                        Brick{ Point{21,7},brickHeight,brickHeight,6 },
                        Brick{ Point{21,8},brickHeight,brickHeight,5 },
                        Brick{ Point{22,6},brickHeight,brickHeight,6 },
                        Brick{ Point{23,6},brickHeight,brickHeight,5 },
                };
    }
}  // namespace arkanoid