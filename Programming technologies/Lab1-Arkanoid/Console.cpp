#include "Console.h"

#include <cstdlib>

#include <conio.h>
#include <Windows.h>
#include <WinUser.h>

namespace console {

    void resize(std::size_t x, std::size_t y)
    {
        HWND console = GetConsoleWindow();
        RECT r;
        GetWindowRect(console, &r); //stores the console's current dimensions
        MoveWindow(console, r.left, r.top, x, y, true);
    }

    void putCursorToStartOfConsole()
    {
        HANDLE hOut;
        COORD Position;

        hOut = GetStdHandle(STD_OUTPUT_HANDLE);

        Position.X = 0;
        Position.Y = 0;
        SetConsoleCursorPosition(hOut, Position);
    }


    void clearScreen()
    {
        std::system("cls");
    }

    bool keyWasPressed()
    {
        return static_cast<bool>(_kbhit());
    }

    char getKey()
    {
        return _getch();
    }

    bool leftKeyHoldDown()
    {
        return isKeyDown(VK_LEFT);
    }

    bool rightKeyHoldDown()
    {
        return isKeyDown(VK_RIGHT);
    }

    bool spaceKeyHoldDown()
    {
        return isKeyDown(VK_SPACE);
    }

    bool escKeyHoldDown()
    {
        return isKeyDown(VK_ESCAPE);
    }

    bool rKeyHoldDown()
    {
        return isKeyDown(0x52);
    }

    bool isKeyDown(int key_code)
    {
        return GetAsyncKeyState(key_code) & -32768;
    }
}