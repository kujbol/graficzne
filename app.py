from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color

from objects.line import Line

from uix.basics import load_settings, BasicSettings
from uix.polygon_settings import PolygonSettingsWidget
from uix.viewer_settings import ViewerSettingsWidget




class MyPaintWidget(BoxLayout):

    object_set = set()
    point_set = set()

    selected_obj = None
    selected_point = None
    selected_method = Line

    object_settings_box = ObjectProperty()
    additional_settings_box = ObjectProperty()

    settings_widgets = [PolygonSettingsWidget(), ViewerSettingsWidget()]

    saved_color = None

    def on_touch_down(self, touch):
        x, y = int(touch.x), int(touch.y)
        is_touched = any(point.on_touch_down(x, y) for point in self.point_set)
        if not is_touched and x > self.children[0].x:
            obj = self.selected_method(x, y, self)
            if obj:
                self.object_set.add(obj)
                self.select_obj(obj)
        else:
            for child in self.children:
                child.on_touch_down(touch)

    def on_touch_move(self, touch):
        x, y = int(touch.x), int(touch.y)
        if x > self.children[0].x:
            for point in self.point_set:
                point.on_touch_move(x, y)

    def on_touch_up(self, touch):
        x, y = int(touch.x), int(touch.y)
        for point in self.point_set:
            point.on_touch_up(x, y)

    def on_press_button(self, class_object):
        self.selected_method = class_object

    def on_update_settings(self, edit, typ=None):
        if not self.selected_obj:
            return
        if isinstance(edit, CheckBox):
            self.selected_obj.settings.anty_aliasing = edit.active
        else:
            if typ == 'color' and edit.text != '':
                try:
                    r, g, b = edit.text.split(' ')
                    self.selected_obj.settings.color = Color(r, g, b)
                    self.saved_color = Color(r, g, b)
                except ValueError:
                    pass
            elif typ == 'thickness' and edit.text != '':
                try:
                    self.selected_obj.settings.thickness = int(edit.text)
                except ValueError:
                    pass
        if self.selected_obj:
            self.selected_obj.draw()

    def select_obj(self, obj):
        if self.selected_obj:
            self.selected_obj.settings.color = self.saved_color
            self.selected_obj.draw()

        self.selected_obj = obj

        load_settings(self, obj)

        self.selected_obj.draw()

    def remove_active_obj(self):
        if self.selected_obj:
            self.selected_obj.delete()
            self.selected_obj = None

        self.additional_settings_box.clear_widgets()




class MyPaintApp(App):

    def build(self):
        return Builder.load_file("app_layout.kv")

if __name__ == '__main__':
    app = MyPaintApp()
    app.run()
