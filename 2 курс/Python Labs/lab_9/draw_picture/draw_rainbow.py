import simple_draw as sd
sd.resolution = (1200, 600)

def rainbow():
    rainbow_colors = (sd.COLOR_RED, sd.COLOR_ORANGE, sd.COLOR_YELLOW, sd.COLOR_GREEN,
                      sd.COLOR_CYAN, sd.COLOR_BLUE, sd.COLOR_PURPLE)
    point = sd.get_point(1000, 0)
    radius = 400
    for i in range(len(rainbow_colors)):
        radius -= 5
        sd.circle(center_position=point, radius=radius, color=rainbow_colors[i], width=4)