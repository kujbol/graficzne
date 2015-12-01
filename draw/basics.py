from math import sqrt
from kivy.graphics import Ellipse
from kivy.graphics.context_instructions import Color
from kivy.graphics.instructions import InstructionGroup


def put_pixel(x, y, color, canvas, token, alpha=None, thickness=2):
    r, g, b = color.r, color.g, color.b
    c = Color(r, g, b)
    if alpha:
        c.a = alpha
    group = InstructionGroup(group=token)
    group.add(c)
    group.add(Ellipse(pos=(x, y), size=(thickness, thickness)))

    canvas.add(group)


def fpart(x):
    return x - int(x)


def rfpart(x):
    return 1 - fpart(x)


def sign(x):
    if x >= 0:
        return 1
    else:
        return -1

def length(x1, y1, x2, y2):
    return sqrt((x1 - x2)*(x1 - x2) + (y1 - y2)*(y1 - y2))