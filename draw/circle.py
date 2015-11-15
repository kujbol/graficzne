from math import ceil, sqrt
from draw.basics import length, put_pixel


def draw_circle(x1, y1, x2, y2, color, obj=None, canvas=None, thickness=1):

    canvas = canvas or obj.widget.canvas
    token = str(hash(obj))

    r = length(x1, y1, x2, y2)
    delta_E = 3
    delta_SE = 5 - 2*r
    d = 1 - r
    x = 0
    y = r

    put_pixel(x+x1, y+y1, color, canvas, token, thickness=thickness)
    while y > x:
        if d < 0:
            d += delta_E
            delta_E += 2
            delta_SE += 2
        else:
            d += delta_SE
            delta_E += 2
            delta_SE += 4
            y -= 1
        x += 1
        put_pixel(x + x1, y + y1, color, canvas, token, thickness=thickness)
        put_pixel(y + x1, x + y1, color, canvas, token, thickness=thickness)
        put_pixel(y + x1, -x + y1, color, canvas, token, thickness=thickness)
        put_pixel(x + x1, -y + y1, color, canvas, token, thickness=thickness)
        put_pixel(-x + x1, y + y1, color, canvas, token, thickness=thickness)
        put_pixel(-y + x1, -x + y1, color, canvas, token, thickness=thickness)
        put_pixel(-y + x1, x + y1, color, canvas, token, thickness=thickness)
        put_pixel(-x + x1, -y + y1, color, canvas, token, thickness=thickness)


def draw_circle_anty_aliasing(
        x1, y1, x2, y2, color, obj=None, canvas=None, thickness=1
):

    canvas = canvas or obj.widget.canvas
    token = str(hash(obj))

    r = length(x1, y1, x2, y2)
    x = r
    y = 0
    t = 0

    D = lambda r, y: ceil(sqrt(r*r - y*y)) - sqrt(r*r - y*y)

    def put_pixel_alphed(x, y, color, canvas, token, alpha, thickness):
        put_pixel(x, y, color, canvas, token, alpha=1 - alpha, thickness=thickness)
        put_pixel(x-1, y, color, canvas, token, alpha=alpha, thickness=thickness)
    while x > y:
        y += 1
        if D(r, y) < t:
            x -= 1
        put_pixel_alphed(x+x1, y+y1, color, canvas, token, alpha=D(r, y), thickness=thickness)
        put_pixel_alphed(y+x1, x+y1, color, canvas, token, alpha=D(r, y), thickness=thickness)
        put_pixel_alphed(y+x1, -x+y1, color, canvas, token, alpha=D(r, y), thickness=thickness)
        put_pixel_alphed(x+x1, -y+y1, color, canvas, token, alpha=D(r, y), thickness=thickness)
        put_pixel_alphed(-x+x1, -y+y1, color, canvas, token, alpha=1-D(r, y), thickness=thickness)
        put_pixel_alphed(-y+x1, -x+y1, color, canvas, token, alpha=1-D(r, y), thickness=thickness)
        put_pixel_alphed(-y+x1, x+y1, color, canvas, token, alpha=1-D(r, y), thickness=thickness)
        put_pixel_alphed(-x+x1, y+y1, color, canvas, token, alpha=1-D(r, y), thickness=thickness)
        t = D(r, y)
