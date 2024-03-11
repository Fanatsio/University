import turtle


WIDTH, HEIGHT = 1000, 800
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor('black')
screen.delay(0)

tutle = turtle.Turtle()
tutle.speed(0)
tutle.color('magenta')

gens = 13
axiom = 'FX'
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
    for chr in axiom:
        if chr == chr_1 or chr == chr_2:
            tutle.forward(step)
        elif chr == '+':
            tutle.right(angle)
        elif chr == '-':
            tutle.left(angle)


axiom = get_result(gens, axiom)
draw_l_system(axiom)

screen.exitonclick()
