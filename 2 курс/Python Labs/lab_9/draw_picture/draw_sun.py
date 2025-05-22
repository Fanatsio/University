import simple_draw as sd

def sun():
    center = sd.get_point(100, 500)
    sd.circle(center, width=0, color=sd.COLOR_YELLOW, radius=50)
    for angle in range(0, 361, 30):
        vec = sd.get_vector(center, angle=angle, width=4, length=100)
        vec.draw()
