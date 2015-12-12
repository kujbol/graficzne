from kivy.graphics.context_instructions import Color
from calculations.basics import SimplePoint, Segment, is_between
from calculations.vec3d import Vec3d
from draw.basics import put_pixel
from draw.line import draw_line
from textures.phong_model import get_light_phong


def re_draw_polygon_inside(
        polygon, texture=None, lights=None, viewer=None, min_x=None, min_y=None,
        bump_map=None
):
    clean_polygon_inside(polygon)
    polygon.token_inside = object()

    token_obj = polygon.token_inside
    color = Color(0, 0, 0)
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
                if texture and lights and viewer:
                    for j in range(int(i2.x), int(i1.x)):
                        r, g, b = texture.getpixel((j - min_x, i - min_y))
                        if bump_map:
                            r1, g1, b1 = bump_map.getpixel((j - min_x, i - min_y))
                            norm = Vec3d(r1/128.0 - 1, g1/128.0 - 1, b1/128.0 - 1)
                        else:
                            norm = None
                        color = Color(
                            float(r)/255 *
                            get_light_phong(j, i, viewer, lights, norm=norm),
                            float(g)/255 *
                            get_light_phong(j, i, viewer, lights, norm=norm),
                            float(b)/255 *
                            get_light_phong(j, i, viewer, lights, norm=norm)
                        )
                        put_pixel(
                            j, i, color, canvas, str(hash(token_obj))
                        )
                elif texture:
                    for j in range(int(i2.x), int(i1.x)):
                        r, g, b = texture.getpixel((j - min_x, i - min_y))
                        color = Color(float(r)/255, float(g)/255, float(b)/255)
                        put_pixel(
                            j, i, color, canvas, str(hash(token_obj))
                        )
                elif lights and viewer:
                    for j in range(int(i2.x), int(i1.x)):
                        color = Color(
                            get_light_phong(j, i, viewer, lights),
                            get_light_phong(j, i, viewer, lights),
                            get_light_phong(j, i, viewer, lights)
                        )
                        put_pixel(
                            j, i, color, canvas, str(hash(token_obj))
                        )
                else:
                    draw_line(
                        int(i1.x), i, int(i2.x), i, color, obj=token_obj, canvas=canvas
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
