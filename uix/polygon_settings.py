from kivy.uix.button import Button

from uix.basics import BasicSettingWidgetClass
from objects.polygon import Polygon


def add_point_to_polygon(x, y, widget):
    print x, y, widget


class PolygonSettingsWidget(BasicSettingWidgetClass):
    setting_class = Polygon
    requirements = []

    def add_settings(self, widget):
        self.remove_settings(widget)

        object_settings_box = widget.additional_settings_box

        add_point_btn = Button(text='Add point to poly')
        add_point_btn.bind(
            on_press=widget.on_press_button(add_point_to_polygon)
        )

        remove_point_btn = Button(text='Remove active point from poly')
        # self.remove_point_btn.bind(on_press=widget.on_press_button('RemovePoint'))

        object_settings_box.add_widget(add_point_btn)
        object_settings_box.add_widget(remove_point_btn)

