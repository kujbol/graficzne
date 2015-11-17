from itertools import chain
from calculations.basics import Segment
from draw.line import draw_line, draw_line_anty_aliasing
from draw.polygon import clean_polygon_inside, re_draw_polygon_inside

from objects.basics import Settings, BasicPointClass
from objects.point import Point


def add_inter_points(graph, intersection_points, segments):
    for segment in segments:
        polygon_intersection_points = []
        for intersection_point in intersection_points:
            if segment.direction(intersection_point) == 0:
                polygon_intersection_points.append(intersection_point)
        polygon_intersection_points.sort(
            key=lambda p: segment.p1.distance(p), reverse=True
        )
        previous = segment.p1
        for point in polygon_intersection_points:
            graph[previous].apend(point)
        graph[point] = segment.p2


class Polygon(BasicPointClass):
    def __init__(self, x, y, widget):
        self.widget = widget
        self.token_inside = None
        self.settings = Settings()
        self.points = [
            Point(x, y, self), Point(x + 30, y + 30, self),
            Point(x + 30, y - 30, self),
        ]

        self.widget.selected_point = self.points[0]

        self.draw()

    def draw(self):
        self.widget.canvas.remove_group(str(hash(self)))
        clean_polygon_inside(self)

        p2 = self.points[-1]
        for point in self.points:
            p1 = p2
            p2 = point
            self._draw_line(p1, p2)

    def _draw_line(self, point1, point2):
        x1, y1 = point1.x, point1.y
        x2, y2 = point2.x, point2.y
        if not self.settings.anty_aliasing:
            draw_line(
                x1, y1, x2, y2, self.settings.color, obj=self,
                thickness=self.settings.thickness
            )
        else:
            draw_line_anty_aliasing(
                x1, y1, x2, y2, self.settings.color, obj=self,
                thickness=self.settings.thickness
            )

    def add_point(self, x, y, widget):
        clean_polygon_inside(self)
        point = Point(x, y, self)
        self.points.append(point)
        widget.selected_point = point
        self.draw()

    def move_active_point(self, widget):
        clean_polygon_inside(self)
        try:
            index = self.points.index(widget.selected_point)
        except ValueError:
            pass
        else:
            self.points[index], self.points[index-1] = (
                self.points[index-1], self.points[index]
            )
            self.draw()

    def change_fill(self, widget):
        if self.token_inside:
            clean_polygon_inside(self)
        else:
            re_draw_polygon_inside(self)

    def find_intersection_with_polygon(self, polygon):
        polygon_segments = [
            Segment(p1, p2)
            for p1, p2 in zip(polygon.points[:-1], polygon.points[1:])
        ]
        polygon_segments.append(Segment(polygon.points[-1], polygon.points[0]))

        self_segments = [
            Segment(p1, p2)
            for p1, p2 in zip(self.points[:-1], self.points[1:])
        ]
        self_segments.append(Segment(self.points[-1], self.points[0]))

        intersection_points = [
            Segment.intersection(self_segment, segment)
            for segment in polygon_segments
            for self_segment in self_segments
            if Segment.is_intersection(self_segment, segment)
        ]

        graph = {
            segment.p1: []
            for segment in chain(polygon_segments, self_segments)
        }

        for point in intersection_points:
            graph[point] = []

        add_inter_points(graph, intersection_points, polygon_segments)
        add_inter_points(graph, intersection_points, self_segments)

        visited = {
            obj: False for obj in graph.iterkeys()
        }

