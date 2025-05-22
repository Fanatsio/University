import simple_draw as sd

def tree():
    def draw_branches(start_point, angle, length):
        if length < 3:
            return
        vec1 = sd.get_vector(start_point, angle + 30, length)
        vec1.draw() if length > 10 else vec1.draw(color=sd.COLOR_GREEN)
        vec2 = sd.get_vector(start_point, angle - 30, length)
        vec2.draw() if length > 10 else vec2.draw(color=sd.COLOR_GREEN)
        draw_branches(vec1.end_point, angle + sd.random_number(18, 42), length * sd.random_number(6, 9) / 10)
        draw_branches(vec2.end_point, angle - sd.random_number(18, 42), length * sd.random_number(6, 9) / 10)
    sd.line(sd.get_point(950, 100), sd.get_point(950, 19))
    root_point = sd.get_point(950, 100)
    draw_branches(start_point=root_point, angle=90, length=50)