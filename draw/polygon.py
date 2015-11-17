from kivy.graphics.context_instructions import Color
from calculations.basics import SimplePoint, Segment
from draw.line import draw_line


def re_draw_polygon_inside(polygon):
    clean_polygon_inside(polygon)
    polygon.token_inside = object()

    token_obj = polygon.token_inside
    color = Color(0, 1, 0)
    canvas = polygon.widget.canvas

    segments = [
        Segment(p1, p2)
        for p1, p2 in zip(polygon.points[:-1], polygon.points[1:])
    ]
    segments.append(Segment(polygon.points[-1], polygon.points[0]))

    mini = min(point.y for point in polygon.points)
    maxi = max(point.y for point in polygon.points)
    for i in range(mini, maxi):
        actual_line = Segment(SimplePoint(x=200, y=i), SimplePoint(x=800, y=i))

        intersections = [
            Segment.intersection(actual_line, segment) for segment in segments
            if Segment.is_intersection(actual_line, segment)
        ]
        intersections.sort(key=lambda point: point.x, reverse=True)
        if intersections:
            for i1, i2 in zip(intersections[::2], intersections[1::2]):
                draw_line(i1.x, i, i2.x, i, color, obj=token_obj, canvas=canvas)


def clean_polygon_inside(polygon):
    if polygon.token_inside:
        polygon.widget.canvas.remove_group(str(hash(polygon.token_inside)))
    polygon.token_inside = None
