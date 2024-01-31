#include "Game.h"

#include "Console.h"
#include "Level.h"

#include <iostream>

namespace arkanoid {

    bool runGame()
    {
        console::resize(500, 453);

        static constexpr auto startScore = 0;
        static constexpr auto startLives = 3;
        long long score = startScore;
        int lives = startLives;
        int level{ 0 };
        for (;;) {

            Level level1{ score, lives,  ++level, makeBricksLevel1() };
            level1.run();
            score = level1.score();
            lives = level1.lives();

            if (level1.isGameOver()) {
                return userInputGameOver(score);
            }

            Level level2{ level1.score(), level1.lives(),  ++level, makeBricksLevel2() };
            level2.run();
            score = level1.score();
            lives = level1.lives();

            if (level2.isGameOver()) {
                return userInputGameOver(score);
            }
        }
    }

    bool userInputGameOver(long long score)
    {
        console::clearScreen();
        std::cout << "Game Over!!!\n"
                  << "SCORE:" << score<<'\n'
                  << "Press R To Try again or ESC to Quit\n";
        for (;;) {
            if (console::rKeyHoldDown()) {
                return true;
            }
            if (console::escKeyHoldDown()) {
                return false;
            }
        }
        console::clearScreen();
    }
}  // namespace arkanoid