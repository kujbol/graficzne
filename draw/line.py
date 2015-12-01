from draw.basics import put_pixel, sign, rfpart, fpart


def draw_line(x1, y1, x2, y2, color, obj=None, canvas=None, thickness=1):

    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
    canvas = canvas or obj.widget.canvas
    token = str(hash(obj))

    dx = x2-x1
    dy = y2-y1

    inc_x = sign(dx)
    inc_y = sign(dy)

    dx = abs(dx)
    dy = abs(dy)

    if dx >= dy:
        d = 2*dy - dx
        delta_a = 2*dy
        delta_b = 2*dy - 2*dx

        x, y = (0, 0)
        for i in range(dx+1-thickness):
            put_pixel(x1+x, y1+y, color, canvas, token, thickness=thickness)
            if d > 0:
                d += delta_b
                x += inc_x
                y += inc_y
            else:
                d += delta_a
                x += inc_x

    else:
        d = 2*dx - dy
        delta_a = 2*dx
        delta_b = 2*dx - 2*dy

        x, y = (0, 0)
        for i in range(dy+1-thickness):
            put_pixel(x1+x, y1+y, color, canvas, token, thickness=thickness)
            if d > 0:
                d += delta_b
                x += inc_x
                y += inc_y
            else:
                d += delta_a
                y += inc_y


def draw_line_anty_aliasing(
        x1, y1, x2, y2, color, obj=None, canvas=None, thickness=1
):
    canvas = canvas or obj.widget.canvas
    token = str(hash(obj))

    dx = x2-x1
    dy = y2-y1

    if abs(dx) >= abs(dy):
        if x1 > x2:
            draw_line_anty_aliasing(
                x2, y2, x1, y1, color, obj=obj, canvas=canvas,
                thickness=thickness
            )
        grad = float(dy)/float(dx)
        y = y1
        for x in range(x1, x2 - thickness):
            c1, c2 = fpart(y),  rfpart(y)

            put_pixel(
                x, y, color, canvas, token, alpha=c1, thickness=thickness
            )
            put_pixel(
                x, y+1, color, canvas, token, alpha=c2, thickness=thickness
            )

            y += grad
    else:
        if y1 > y2:
            draw_line_anty_aliasing(
                x2, y2, x1, y1, color, obj=obj, canvas=canvas,
                thickness=thickness
            )
        grad = float(dx)/float(dy)
        x = x1
        for y in range(y1, y2 - thickness):
            c1, c2 = fpart(x),  rfpart(x)

            put_pixel(
                x, y, color, canvas, token, alpha=c1, thickness=thickness
            )
            put_pixel(
                x+1, y, color, canvas, token, alpha=c2, thickness=thickness
            )

            x += grad
