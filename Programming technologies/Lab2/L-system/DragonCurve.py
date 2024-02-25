import turtle

# Настройки экрана
WIDTH, HEIGHT = 1600, 900
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.screensize(3 * WIDTH, 3 * HEIGHT)
screen.bgcolor('black')
screen.delay(0)

# Настройки черепахи
leo = turtle.Turtle()
leo.pensize(2)
leo.speed(0)
leo.setpos(WIDTH // 4, -HEIGHT // 4 - 25)
leo.color('magenta')

# Настройки L-системы
gens = 13
axiom = 'XY'
chr_1, rule_1 = 'X', 'X+YF+'
chr_2, rule_2 = 'Y', '-FX-Y'
step = 4
angle = 90


def apply_rules(axiom):
    """Применяет правила L-системы к аксиоме."""
    return ''.join([rule_1 if chr == chr_1 else
                    rule_2 if chr == chr_2 else chr for chr in axiom])


def get_result(gens, axiom):
    """Получает конечную строку L-системы после применения правил."""
    for _ in range(gens):
        axiom = apply_rules(axiom)
    return axiom


def draw_l_system(axiom):
    """Рисует L-систему с помощью черепахи."""
    turtle.penup()
    turtle.goto(-WIDTH // 2 + 60, -HEIGHT // 2 - 100)
    turtle.pendown()

    for chr in axiom:
        if chr == chr_1 or chr == chr_2:
            leo.forward(step)
        elif chr == '+':
            leo.right(angle)
        elif chr == '-':
            leo.left(angle)


# Получение и рисование L-системы
axiom = get_result(gens, axiom)
draw_l_system(axiom)

screen.exitonclick()
