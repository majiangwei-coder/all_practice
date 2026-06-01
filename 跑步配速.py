import math


def run(speed):
    # 1000 * speed / 3600
    speed_every_km = 60 / speed
    return f"当前实时配速为{int(math.modf(speed_every_km)[1])}分{math.modf(speed_every_km)[0] * 60:.2f}秒\n当前配速可较之十公里配速下每公里节省{(1 - math.modf(speed_every_km)[0]) * 60:.2f}秒"
    # return f"当前实时配速为{int(math.modf(speed_every_km)[1])}分{format(math.modf(speed_every_km)[0] * 60, '.2f')}秒"
    # return f"当前实时配速为{int(math.modf(speed_every_km)[1])}分{round(math.modf(speed_every_km)[0] * 60, 2)}秒"


print(run(11.5))