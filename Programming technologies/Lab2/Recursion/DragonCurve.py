import turtle

# Рекурсивный метод для построения кривой дракона
def recursive_dragon_curve(turtle, order, length):
    if order == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, order - 1, length)
        turtle.right(90)
        reverse_dragon_curve(turtle, order - 1, length)

# Рекурсивный метод для построения обратной кривой дракона
def reverse_dragon_curve(turtle, order, length):
    if order == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, order - 1, length)
        turtle.left(90)
        reverse_dragon_curve(turtle, order - 1, length)

# Метод для построения кривой дракона с использованием L-системы
def iterative_dragon_curve(turtle, order, length):
    dragon_curve = "FX"
    dragon_rules = {"X": "X+YF+", "Y": "-FX-Y"}

    # Генерация строки кривой с помощью правил L-системы
    for _ in range(order):
        dragon_curve = "".join([dragon_rules.get(c, c) for c in dragon_curve])

    # Построение кривой на основе сгенерированной строки
    for char in dragon_curve:
        if char == "F":
            turtle.forward(length)
        elif char == "+":
            turtle.right(90)
        elif char == "-":
            turtle.left(90)

# Инициализация экрана и черепашки
screen = turtle.Screen()
screen.setup(width=1280, height=720)
screen.title("Dragon Curve Fractal")
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)  # Ускоряем черепашку

# Рисование рекурсивной кривой дракона
t.penup()
t.goto(-300, 0)
t.pendown()
t.color("blue")
recursive_dragon_curve(t, 12, 5)

# Рисование кривой дракона с использованием L-системы
t.penup()
t.goto(100, 0)
t.pendown()
t.color("red")
iterative_dragon_curve(t, 12, 5)

# Закрытие окна по клику
screen.exitonclick()
