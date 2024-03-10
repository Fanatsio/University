import turtle


def recursive_dragon_curve(turtle, order, length):
    if order == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, order - 1, length)
        turtle.right(90)
        reverse_dragon_curve(turtle, order - 1, length)


def reverse_dragon_curve(turtle, order, length):
    if order == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, order - 1, length)
        turtle.left(90)
        reverse_dragon_curve(turtle, order - 1, length)


screen = turtle.Screen()
screen.setup(width=1280, height=720)
screen.title("Dragon Curve Fractal")
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)

t.penup()
t.goto(-300, 0)
t.pendown()
t.color("blue")
recursive_dragon_curve(t, 12, 5)

screen.exitonclick()
