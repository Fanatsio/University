# -*- coding: utf-8 -*-
import math
def  T_calculation_length(*args):
    return math.ceil(args[0] * args[1] / (args[2] * 0.01) / (args[3] * 0.01))

def  T_calculation_cost(*args):
    return  args[0] * args[1]
