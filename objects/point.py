from kivy.uix.widget import Widget
from draw.point import draw_point, POINT_SIZE
from draw.polygon import clean_polygon_inside


class Point(object):
    def __init__(self, x, y, obj, size=None, texture=None):
        self.x = x
        self.y = y
        self.obj = obj
        self.obj.widget.point_set.add(self)
        self.size = size or POINT_SIZE
        self.texture = texture

        draw_point(self)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        draw_point(self)

        # TODO fix this shit
        if getattr(self.obj, 'token_inside', None):
            clean_polygon_inside(self.obj)

        self.obj.draw()

    def delete(self):

        # TODO fix this shit
        if getattr(self.obj, 'token_inside', None):
            clean_polygon_inside(self.obj)

        self.obj.widget.point_set.remove(self)
        self.obj.widget.canvas.remove_group(str(hash(self)))

    def is_touched(self, x, y):
        return (
            abs(x - self.x) < self.size and
            abs(y - self.y) < self.size
        )

    def on_touch_down(self, x, y):
        if self.is_touched(x, y):
            self.obj.widget.select_obj(self.obj)
            self.obj.widget.selected_point = self
            return True
        return False

    def on_touch_move(self, x, y):
        if self.obj.widget.selected_point is self:
            self.update_position(x, y)

    def on_touch_up(self, x, y):
        pass
        # if self.obj.widget.selected_point is self:
        #     self.obj.widget.selected_point = None

