cmake_minimum_required(VERSION 3.14)
project(IntegralLib)

# Установка стандартов для C и C++
set(CMAKE_C_STANDARD 99)
set(CMAKE_CXX_STANDARD 17)

# Опции для 32-битной и 64-битной компиляции
set(CMAKE_C_FLAGS_32 "-m32")
set(CMAKE_CXX_FLAGS_32 "-m32")

# Ваш исходный файл
set(SOURCE_FILES integral.cpp)

# Создание библиотеки для 64-битной Windows
add_library(integral64 SHARED ${SOURCE_FILES})
set_target_properties(integral64 PROPERTIES OUTPUT_NAME "integral64")

# Создание библиотеки для 32-битной Windows
add_library(integral32 SHARED ${SOURCE_FILES})
set_target_properties(integral32 PROPERTIES OUTPUT_NAME "integral32")
target_compile_options(integral32 PRIVATE ${CMAKE_C_FLAGS_32} ${CMAKE_CXX_FLAGS_32})

# Создание библиотеки для 64-битной Linux
add_library(integral64_linux SHARED ${SOURCE_FILES})
set_target_properties(integral64_linux PROPERTIES OUTPUT_NAME "integral64_linux")

# Создание библиотеки для 32-битной Linux
add_library(integral32_linux SHARED ${SOURCE_FILES})
set_target_properties(integral32_linux PROPERTIES OUTPUT_NAME "integral32_linux")
target_compile_options(integral32_linux PRIVATE ${CMAKE_C_FLAGS_32} ${CMAKE_CXX_FLAGS_32})
