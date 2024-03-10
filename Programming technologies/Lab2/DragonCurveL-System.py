import turtle

WIDTH, HEIGHT = 1600, 900
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(3 * WIDTH, 3 * HEIGHT)
screen.bgcolor('black')
screen.delay(0)

turtl = turtle.Turtle()
turtl.pensize(2)
turtl.speed(0)
turtl.setpos(WIDTH // 4, -HEIGHT // 4 - 25)
turtl.color('magenta')

gens = 13
axiom = 'XY'
chr_1, rule_1 = 'X', 'X+YF+'
chr_2, rule_2 = 'Y', '-FX-Y'
step = 4
angle = 90


def apply_rules(axiom):
    return ''.join([rule_1 if chr == chr_1 else
                    rule_2 if chr == chr_2 else chr for chr in axiom])


def get_result(gens, axiom):
    for _ in range(gens):
        axiom = apply_rules(axiom)
    return axiom


def draw_l_system(axiom):
    turtle.penup()
    turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 - 100)
    turtle.pendown()

    for chr in axiom:
        if chr == chr_1 or chr == chr_2:
            turtl.forward(step)
        elif chr == '+':
            turtl.right(angle)
        elif chr == '-':
            turtl.left(angle)


axiom = get_result(gens, axiom)
draw_l_system(axiom)

screen.exitonclick()
