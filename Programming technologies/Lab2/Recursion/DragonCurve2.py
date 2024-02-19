from turtle import Turtle, Screen


R = "R"
L = "L"

def iterate(sequence: str) -> str:
    sequence = sequence+R+swapLetters(sequence[::-1])
    return sequence


def swapLetters(sequence: str) -> str:
    newSequence = ""
    for letter in sequence:
        if letter == R:
            newSequence = newSequence + L
        else:
            newSequence = newSequence + R
    return newSequence


def dragon(n_iterations: int) -> str:
    initial_sequence = R
    for i in range(0, n_iterations):
        initial_sequence = iterate(initial_sequence)
    return initial_sequence


# Turtle setup
turtle = Turtle("turtle")
turtle.hideturtle()
turtle.speed(0)
turtle.color("#ff69aa")

# Screen setup
screen = Screen()
screen.title("Dragon Curve")
screen.bgcolor("black")
screen.screensize(1920*3, 1080*3)
screen.setup(width=1.0, height=1.0, startx=None, starty=None)


# Draw
LENGTH = 5
turtle.forward(LENGTH)
for element in dragon(17):
    if element == R:
        turtle.right(90)
        turtle.forward(LENGTH)
    else:
        turtle.left(90)
        turtle.forward(LENGTH)
        
'''
# Draw with circle
LENGTH = 5
for element in dragon(17):
    if element == R:
        turtle.circle(-4, 90, 36)
    else:
        turtle.circle(4, 90, 36)
'''

# When finished, click to exit
turtle.color("white")
turtle.write("click to exit", font=("Calibri", 16, "bold"))
screen.exitonclick()