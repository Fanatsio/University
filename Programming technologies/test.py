import turtle

def recursive_dragon_curve(tutle, order, length):
    if order == 0:
        tutle.forward(length)
    else:
        recursive_dragon_curve(tutle, order - 1, length)
        tutle.right(90)
        reverse_dragon_curve(tutle, order - 1, length)

def reverse_dragon_curve(tutle, order, length):
    if order == 0:
        tutle.forward(length)
    else:
        recursive_dragon_curve(tutle, order - 1, length)
        tutle.left(90)
        reverse_dragon_curve(tutle, order - 1, length)


screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.title("Dragon Curve Fractal")
screen.bgcolor("white")

turtle = turtle.Turtle()
turtle.speed(0)

turtle.penup()
turtle.goto(-300, 0)
turtle.pendown()
turtle.color("blue")
recursive_dragon_curve(turtle, 12, 4)

screen.exitonclick()