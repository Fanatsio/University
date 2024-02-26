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

# Закрытие окна по клику
screen.exitonclick()
