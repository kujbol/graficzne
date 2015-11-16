from draw.line import draw_line, draw_line_anty_aliasing

from objects.basics import Settings, BasicPointClass
from objects.point import Point


class Line(BasicPointClass):
    def __init__(self, x, y, widget):
        self.widget = widget
        self.settings = Settings()
        self.points = [Point(x, y, self), Point(x+30, y, self)]

        self.widget.selected_point = self.points[0]

        self.draw()

    def draw(self):
        x1, y1 = self.points[0].x, self.points[0].y
        x2, y2 = self.points[1].x, self.points[1].y
        self.widget.canvas.remove_group(str(hash(self)))
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
