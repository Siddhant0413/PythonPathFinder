import random
import math
from Cell import Cell

class Fire:
    def __init__(fire, cell):
        fire.cell = cell
        fire.cell.on_fire = True