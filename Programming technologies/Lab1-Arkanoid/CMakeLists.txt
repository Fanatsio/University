cmake_minimum_required(VERSION 3.27)
project(Lab1_Arkanoid)

set(CMAKE_CXX_STANDARD 23)

add_executable(Lab1_Arkanoid main.cpp
        Game.h
        Game.cpp
        Level.h
        Level.cpp
        GameObject.h
        GameObject.cpp
        Ball.h
        Ball.cpp
        Brick.h
        Brick.cpp
        Platform.h
        Platform.cpp
        Wall.h
        Wall.cpp
        Point.h
        Time.h
        Time.cpp
        Grid.h
        Grid.cpp
        Console.h
        Console.cpp
        NearlyEqual.h
        NearlyEqual.cpp
        MathHelper.h)
