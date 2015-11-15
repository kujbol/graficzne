from kivy.graphics.context_instructions import Color


class Settings(object):
    color = Color(1, 1, 1)
    thickness = 1
    anty_aliasing = False


class BasicPointClass(object):
    # interface of class
    points = []
    settings = Settings()
    widget = None

    def delete(self):
        for point in self.points:
            point.delete()
        self.widget.canvas.remove_group(str(hash(self)))

