import turtle

def recursive_dragon_curve(turtle, gens, length):
    if gens == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, gens - 1, length)
        turtle.right(90)
        reverse_dragon_curve(turtle, gens - 1, length)

def reverse_dragon_curve(turtle, gens, length):
    if gens == 0:
        turtle.forward(length)
    else:
        recursive_dragon_curve(turtle, gens - 1, length)
        turtle.left(90)
        reverse_dragon_curve(turtle, gens - 1, length)

WIDTH, HEIGHT = 1000, 800
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("white")
screen.delay(0)

tutle = turtle.Turtle()
tutle.speed(0)
tutle.color("blue")

recursive_dragon_curve(tutle, 13, 4)

screen.exitonclick()
