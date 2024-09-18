import math
import random


# x is n/y(t)
def get_equi_no_repacking_servers(x):
    floor_x = math.floor(x)
    ceil_x = math.ceil(x)

    # if x is not a fraction
    if floor_x == ceil_x:
        return floor_x

    # if x is fraction use probability to allocate
    else:
        p = ceil_x - x
        return floor_x if random.random() < p else ceil_x
