# -*- coding: utf-8 -*-
from math import *

def  calculation_quantity(*args):
    roll_square = args[3] * args[4]
    wall_square = 2 * (args[0] * args[2]) + 2 * (args[2] * args[1])
    return wall_square / roll_square
    #wallpaper_strips = args[0] / (args[3] * .1)
    #strips_in_one_roll = args[4] / args[2] 
    #return  wallpaper_strips / strips_in_one_roll

def  calculation_cost(*args):
    return  args[0] * args[1]