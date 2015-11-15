from draw.line import draw_line, draw_line_anty_aliasing

from objects.basics import Settings, BasicPointClass
from objects.point import Point


class Polygon(BasicPointClass):
    def __init__(self, x, y, widget):
        self.widget = widget
        self.settings = Settings()
        self.points = [
            Point(x, y, self), Point(x + 30, y + 30, self),
            Point(x + 30, y - 30, self),
        ]

        self.draw()

    def draw(self):
        self.widget.canvas.remove_group(str(hash(self)))
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
