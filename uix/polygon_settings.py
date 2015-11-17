from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label

from uix.basics import BasicSettingWidgetClass
from objects.polygon import Polygon


class PolygonSettingsWidget(BasicSettingWidgetClass):
    setting_class = Polygon
    requirements = []

    def add_settings(self, widget):
        self.remove_settings(widget)

        object_settings_box = widget.additional_settings_box

        add_point_btn = Button(text='Add point to poly')
        add_point_btn.bind(
            on_press=lambda a: widget.on_press_button(
                widget.selected_obj.add_point
            )
        )

        change_active_point = Button(text='Change active point')
        change_active_point.bind(
            on_press=lambda a: widget.selected_obj.move_active_point(widget)
        )

        fill_polygon = Button(text='Fill polygon')
        fill_polygon.bind(
            on_press=lambda a: widget.selected_obj.change_fill(widget)
        )

        # remove_point_btn = Button(text='Remove active point from poly')
        # self.remove_point_btn.bind(on_press=widget.on_press_button('RemovePoint'))

        object_settings_box.add_widget(add_point_btn)
        object_settings_box.add_widget(change_active_point)
        object_settings_box.add_widget(fill_polygon)
