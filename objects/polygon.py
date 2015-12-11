from itertools import chain
from PIL import Image

from calculations.basics import Segment
from draw.line import draw_line, draw_line_anty_aliasing
from draw.polygon import (
    clean_polygon_inside, re_draw_polygon_inside, create_list
)
from objects.basics import Settings, BasicPointClass
from objects.point import Point
from textures.octree import cut_pallet, closest_color_from_pallet
from textures.popular_pallet import popular_pallet


class Polygon(BasicPointClass):
    def __init__(self, x, y, widget, polygon_point_list=None):
        self.widget = widget
        self.token_inside = None
        self.settings = SettingsPolygon()
        if polygon_point_list:
            self.points = []
            for point in polygon_point_list:
                self.points.append(Point(point.x, point.y, self))
        else:
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

    def draw_texture(self, widget):
        clean_polygon_inside(self)

        max_x = max(point.x for point in self.points)
        max_y = max(point.y for point in self.points)
        min_x = min(point.x for point in self.points)
        min_y = min(point.y for point in self.points)

        im = Image.open('files/3.png')
        im.load()

        if self.settings.popular_model:
            pallet = popular_pallet(im, self.settings.color_count+1)
        else:
            pallet = cut_pallet(im, self.settings.color_count)
        array = list(im.getdata())
        new_array = [
            closest_color_from_pallet(pallet, color)
            for color in array
        ]
        im = Image.new(im.mode, im.size)
        im.putdata(new_array)
        im = im.rotate(180)

        resided = im.resize((max_x - min_x, max_y - min_y))

        rgb_im = resided.convert('RGB')
        re_draw_polygon_inside(self, texture=rgb_im, min_x=min_x, min_y=min_y)

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
        re_draw_polygon_inside(self)

    def set_color_count(self, data):
        try:
            self.settings.color_count = int(data)
        except ValueError:
            pass

    def set_model(self, data):
        self.settings.popular_model = data

    def count_intersection_with_all(self, widget):
        for obj in widget.object_set:
            if isinstance(obj, Polygon):
                self.find_intersection_with_polygon(obj)
                return

    def delete_active_point(self, widget):
        if len(self.points) == 1:
            return
        try:
            i = self.points.index(widget.selected_point)
        except ValueError:
            pass
        else:
            self.points.pop(i)
            widget.selected_point.delete()
            widget.selected_point = None
            self.draw()

    def find_intersection_with_polygon(self, subject):
        # self is window
        subject_segments = [
            Segment(p1, p2)
            for p1, p2 in zip(subject.points[:-1], subject.points[1:])
        ]
        subject_segments.append(Segment(subject.points[-1], subject.points[0]))

        self_segments = [
            Segment(p1, p2)
            for p1, p2 in zip(self.points[:-1], self.points[1:])
        ]
        self_segments.append(Segment(self.points[-1], self.points[0]))

        intersection_points = []
        for self_segment in self_segments:
            for subject_segment in subject_segments:
                if (
                    Segment.is_intersection(self_segment, subject_segment)
                    is True and
                    Segment.intersection(self_segment, subject_segment)
                    is not None
                ):
                    intersection_points.append(
                        Segment.intersection(subject_segment, self_segment)
                    )
        # for point in intersection_points:
        #     Point(point.x, point.y, self)
        print len(intersection_points)

        subject_points = create_list(intersection_points, subject_segments)
        self_points = create_list(intersection_points, self_segments)
        into_self_windows = []  # list of input into window

        i = 0
        for point in self_points:
            if point in intersection_points and i == 0:
                into_self_windows.append(point)
                i = (i + 1) % 2

        visited = {
            point: False
            for point in chain(subject_points, self_points)
        }

        start_point = into_self_windows[0]
        actual_index = subject_points.index(start_point)
        actual_index = (actual_index + 1) % len(subject_points)
        actual_point = subject_points[actual_index]
        output_point_list = [start_point]

        actual_poly = self_points

        def not_actual_poly(actual_poly):
            if actual_poly == subject_points:
                return self_points
            else:
                return subject_points

        while actual_point != start_point:
            if visited[actual_point]:
                break
            visited[actual_point] = True
            output_point_list.append(actual_point)
            if actual_point in not_actual_poly(actual_poly):
                actual_poly = not_actual_poly(actual_poly)
                actual_index = actual_poly.index(actual_point)
                actual_index = (actual_index + 1) % len(actual_poly)
                actual_point = actual_poly[actual_index]
            else:
                actual_index = (actual_index + 1) % len(actual_poly)
                actual_point = actual_poly[actual_index]

        output_poly = Polygon(
            None, None, self.widget, polygon_point_list=output_point_list
        )
        self.widget.selected_obj = output_poly
        self.widget.object_set.add(output_poly)

        # for point1, point2 in zip(output_point_list, output_point_list[1:]):
        #     self._draw_line(point1, point2)
        # self._draw_line(output_point_list[-1], output_point_list[0])


class SettingsPolygon(Settings):
    def __init__(self):
        super(SettingsPolygon, self).__init__()
        self.color_count = 64
        self.popular_model = False

