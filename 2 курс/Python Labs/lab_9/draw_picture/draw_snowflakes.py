import simple_draw as sd

'''def snowflakes():
    N = 20
    len = [sd.random_number(10, 20) for _ in range(N)]
    x_coord = [i for i in range(100, 201, 5)]
    y_coord = [sd.random_number(25, 40) for _ in range(20)]
    for i in range(N):
        point = sd.get_point(x_coord[i], y_coord[i])
        sd.snowflake(point, length=len[i])'''

width = 1200
height = 800
sd.resolution = (width, height)
N = 20

def snowflake_gen():
    return {'length': sd.random_number(8, 24),
            'x': sd.randint(0, 200),
            'y': sd.randint(300, 320),
            'factor_a': sd.random_number(4, 7) / 10,
            'factor_b': sd.random_number(4, 7) / 10,
            'factor_c': sd.random_number(45, 60)
            }

def snowflakes():
    snowflakes = []
    for _ in range(N):
        snowflakes.append(snowflake_gen())
    i = 0
    sd.start_drawing()
    while True:
        for snowflake in snowflakes:
            point = sd.get_point(snowflake['x'], snowflake['y'])
            sd.snowflake(
                point, snowflake['length'],
                sd.background_color,
                snowflake['factor_a'],
                snowflake['factor_b'],
                snowflake['factor_c'])
            snowflake['x'] -= sd.randint(-10, 10)
            snowflake['y'] -= sd.randint(10, 25)
            point = sd.get_point(snowflake['x'], snowflake['y'])
            sd.snowflake(
                point, snowflake['length'],
                sd.COLOR_WHITE,
                snowflake['factor_a'],
                snowflake['factor_b'],
                snowflake['factor_c'])
            if snowflake['y'] < sd.randint(0, 40):
                snowflakes.remove(snowflake)
        i += 1
        if i % 2 == 0:
            new_snowflake = snowflake_gen()
            snowflakes.append(snowflake_gen())
        sd.finish_drawing()
        sd.sleep(0.1)
        if sd.user_want_exit():
            break