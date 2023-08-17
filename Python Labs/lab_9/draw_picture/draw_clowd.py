import simple_draw as sd
sd.resolution = (1200, 600)

def cloud():
    radius = 30
    sd.circle(center_position=sd.get_point(100, 400), radius=radius, color=sd.COLOR_WHITE, width=0)
    sd.circle(center_position=sd.get_point(60, 380), radius=radius, color=sd.COLOR_WHITE, width=0)
    sd.circle(center_position=sd.get_point(100, 380), radius=radius, color=sd.COLOR_WHITE, width=0)
    sd.circle(center_position=sd.get_point(140, 380), radius=radius, color=sd.COLOR_WHITE, width=0)