#include "Game.h"

#include <iostream>

int main() {
    try {
        while (arkanoid::runGame());
    }

    catch (const std::out_of_range& e) {
        std::cerr << e.what() << "\n";
        std::cin.get();
    }

    catch (const std::invalid_argument& e) {
        std::cerr << e.what() << "\n";
        std::cin.get();
    }

    catch (...) {
        std::cerr << "unknown error " << "\n";
        std::cin.get();
    }

    return 0;
}
