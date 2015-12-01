from kivy.graphics.context_instructions import Color
from calculations.basics import SimplePoint, Segment, is_between
from draw.basics import put_pixel
from draw.line import draw_line


def re_draw_polygon_inside(polygon, texture=None, min_x=None, min_y=None):
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
        actual_line = Segment(SimplePoint(x=0, y=i), SimplePoint(x=1000, y=i))

        intersections = [
            Segment.intersection(actual_line, segment) for segment in segments
            if Segment.is_intersection(actual_line, segment)
        ]
        intersections.sort(key=lambda point: point.x, reverse=True)
        if intersections:
            for i1, i2 in zip(intersections[::2], intersections[1::2]):
                if texture:
                    for j in range(i2.x, i1.x):
                        r, g, b = texture.getpixel((j - min_x, i - min_y))
                        color = Color(float(r)/255, float(g)/255, float(b)/255)
                        put_pixel(
                            j, i, color, canvas, str(hash(token_obj))
                        )
                else:
                    draw_line(
                        i1.x, i, i2.x, i, color, obj=token_obj, canvas=canvas
                    )


def clean_polygon_inside(polygon):
    if polygon.token_inside:
        polygon.widget.canvas.remove_group(str(hash(polygon.token_inside)))
    polygon.token_inside = None


def create_list(intersection_points, segments):
    polygon = []
    for segment in segments:
        polygon_intersection_points = []
        for intersection_point in intersection_points:
            if is_between(segment.p1, segment.p2, intersection_point) is True:
                polygon_intersection_points.append(intersection_point)
        polygon_intersection_points.sort(
            key=lambda p: segment.p1.distance(p), reverse=True
        )
        polygon.append(segment.p1)
        if len(polygon_intersection_points) > 0:
            polygon.extend(polygon_intersection_points)
    return polygon
