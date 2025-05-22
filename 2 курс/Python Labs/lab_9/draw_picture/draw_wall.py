import simple_draw as sd

def wall():
    diff = -20
    flag = 1
    for y in range(0, 181, 20):
        diff += 20 * flag
        flag *= -1
        for x in range(300, 601, 40):
            sd.rectangle(sd.get_point(x - 40 - diff, y - 20), sd.get_point(x - diff, y), color=sd.COLOR_ORANGE, width=2)
    sd.line(sd.get_point(260, 0), sd.get_point(260, 180), color=sd.COLOR_ORANGE, width=2)
    sd.line(sd.get_point(600, 0), sd.get_point(600, 180), color=sd.COLOR_ORANGE, width=2)
    sd.line(sd.get_point(260, 180), sd.get_point(600, 180), color=sd.COLOR_ORANGE, width=2)
    sd.line(sd.get_point(260, 1), sd.get_point(600, 1), color=sd.COLOR_ORANGE, width=2)
    v1 = sd.get_vector(sd.get_point(250, 180), length=200, angle=30, width=2)
    sd.polygon([sd.get_point(250, 180), v1.end_point, sd.get_point(610, 180)], color=sd.COLOR_RED, width=0)
    sd.polygon([sd.get_point(0, 0), sd.get_point(0, 19), sd.get_point(1200, 19), sd.get_point(1200, 0)], color=sd.COLOR_DARK_YELLOW, width=0)