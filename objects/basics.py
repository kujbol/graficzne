from kivy.graphics.context_instructions import Color


class Settings(object):
    def __init__(self):
        self.color = Color(0, 0, 0)
        self.thickness = 1
        self.anty_aliasing = False


class BasicPointClass(object):
    # interface of class
    points = []
    settings = Settings()
    widget = None

    def delete(self):
        for point in self.points:
            point.delete()
        self.widget.canvas.remove_group(str(hash(self)))
