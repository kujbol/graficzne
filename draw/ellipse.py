from draw.basics import put_pixel


def draw_ellipse(
        x1, y1, x2, y2, color, obj=None, canvas=None, thickness=1
):

    if y1 < y2:
        draw_ellipse(
            x2, y2, x1, y1, color, obj=obj, canvas=canvas, thickness=thickness
        )
        return

    canvas = canvas or obj.widget.canvas
    token = str(hash(obj))

    x = (x1 - x2) / 2 + x2
    y = (y1 - y2) / 2 + y2
    a = (x1 - x2) / 2
    b = (y1 - y2) / 2

    if (x1 - x2) % 2 == 1:
        mx = 1
    else:
        mx = 0

    if (y1 - y2) % 2 == 1:
        my = 1
    else:
        my = 0

    xc = 0
    yc = b
    aa = a*a
    aa2 = aa + aa
    bb = b*b
    bb2 = bb + bb
    d = bb - aa + b + (aa/4)
    dx = 0
    dy = aa2 * b

    while dx < dy:
        put_pixel(x - xc, y - yc, color, canvas, token, thickness=thickness)
        put_pixel(x - xc, y + my + yc, color, canvas, token, thickness=thickness)
        put_pixel(x + mx + xc, y - yc, color, canvas, token, thickness=thickness)
        put_pixel(x + mx + xc, y + my + yc, color, canvas, token, thickness=thickness)
        if d > 0:
            yc -= 1
            dy -= aa2
            d -= dy
        xc += 1
        dx += bb2
        d += bb + dx

    d += 3*((aa - bb)/2) - (dx + dy)/2

    while yc >= 0:
        put_pixel(x - xc, y - yc, color, canvas, token, thickness=thickness)
        put_pixel(x - xc, y + my + yc, color, canvas, token, thickness=thickness)
        put_pixel(x + mx + xc, y - yc, color, canvas, token, thickness=thickness)
        put_pixel(x + mx + xc, y + my + yc, color, canvas, token, thickness=thickness)
        if d < 0:
            xc += 1
            dx += bb2
            d += bb + dx
        yc -= 1
        dy -= aa2
        d += aa - dy

