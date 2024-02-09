import turtle


# Рекурсивный метод для построения кривой дракона
def recursive_dragon_curve(tutle, order, length):
    if order == 0:
        tutle.forward(length)
    else:
        recursive_dragon_curve(tutle, order - 1, length)
        tutle.right(90)
        reverse_dragon_curve(tutle, order - 1, length)


# Рекурсивный метод для построения обратной кривой дракона
def reverse_dragon_curve(tutle, order, length):
    if order == 0:
        tutle.forward(length)
    else:
        recursive_dragon_curve(tutle, order - 1, length)
        tutle.left(90)
        reverse_dragon_curve(tutle, order - 1, length)


# Метод для построения кривой дракона с использованием L-системы
def iterative_dragon_curve(tutle, order, length):
    dragon_curve = "FX"
    dragon_rules = {"X": "X+YF+", "Y": "-FX-Y"}

    for _ in range(order):
        dragon_curve = "".join([dragon_rules[c] if c in dragon_rules else c for c in dragon_curve])

    for char in dragon_curve:
        if char == "F":
            tutle.forward(length)
        elif char == "+":
            tutle.right(90)
        elif char == "-":
            tutle.left(90)


# Инициализация экрана и черепашки
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Dragon Curve Fractal")
screen.bgcolor("white")

turtle = turtle.Turtle()
turtle.speed(100)  # Ускоряем черепашку

# Рисование рекурсивной кривой дракона
turtle.penup()
turtle.goto(-300, 0)
turtle.pendown()
turtle.color("blue")
recursive_dragon_curve(turtle, 12, 5)

# Рисование кривой дракона с использованием L-системы
turtle.penup()
turtle.goto(100, 0)
turtle.pendown()
turtle.color("red")
iterative_dragon_curve(turtle, 12, 5)

# Закрытие окна по клику
screen.exitonclick()
