from kivy.core.image import Image

from objects.basics import Settings
from objects.point import Point


class Viewer(object):
    def __init__(self, x, y, widget):
        self.widget = widget
        self.settings = SettingsViewer()
        self.point = Point(
                x, y, self, texture=Image('files/eye.png').texture, size=25
            )

        self.widget.selected_point = self.point

        self.draw()

    def draw(self):
        self.widget.canvas.remove_group(str(hash(self)))

    def delete(self):
        pass

    def change_height(self, value):
        try:
            self.settings.height = int(value)
        except ValueError:
            pass


class SettingsViewer(Settings):
    def __init__(self):
        super(SettingsViewer, self).__init__()
        self.height = 25

    def calculate_settings(self):
        pass
