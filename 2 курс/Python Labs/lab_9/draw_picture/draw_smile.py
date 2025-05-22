import simple_draw as sd

def smile():
    position = sd.get_point(700, 130)
    sd.circle(position, radius=20, color=sd.COLOR_PURPLE, width=1)
    sd.line(sd.get_point(position.x - 10, position.y - 10), sd.get_point(position.x + 10, position.y - 10), color=sd.COLOR_PURPLE,width=2)
    sd.line(sd.get_point(position.x - 10, position.y + 10), sd.get_point(position.x - 10, position.y + 10), color=sd.COLOR_PURPLE,width=2)
    sd.line(sd.get_point(position.x + 10, position.y + 10), sd.get_point(position.x + 10, position.y + 10), color=sd.COLOR_PURPLE,width=2)
    sd.line(sd.get_point(700, 110), sd.get_point(700, 60), color=sd.COLOR_PURPLE, width=1)
    sd.line(sd.get_point(680, 19), sd.get_point(700, 60), color=sd.COLOR_PURPLE, width=1)
    sd.line(sd.get_point(720, 19), sd.get_point(700, 60), color=sd.COLOR_PURPLE, width=1)
    sd.line(sd.get_point(700, 90), sd.get_point(680, 70), color=sd.COLOR_PURPLE, width=1)
    sd.line(sd.get_point(700, 90), sd.get_point(720, 70), color=sd.COLOR_PURPLE, width=1)