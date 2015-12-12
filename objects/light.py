from kivy.core.image import Image

from objects.point import Point
from objects.viewer import Viewer, SettingsViewer


class Light(Viewer):
    def __init__(self, x, y, widget):
        self.widget = widget
        self.settings = SettingsViewer()
        self.point = Point(x, y, self, size=25)

        self.widget.selected_point = self.point

        self.draw()

    def delete(self):
        pass
