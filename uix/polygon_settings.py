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

        change_active_point_btn = Button(text='Change active point')
        change_active_point_btn.bind(
            on_press=lambda a: widget.selected_obj.move_active_point(widget)
        )

        fill_polygon_btn = Button(text='Fill polygon')
        fill_polygon_btn.bind(
            on_press=lambda a: widget.selected_obj.change_fill(widget)
        )

        find_intersection_btn = Button(text='Find intersection')
        find_intersection_btn.bind(
            on_press=lambda a: widget.selected_obj.count_intersection_with_all(
                widget
            )
        )

        remove_point_btn = Button(text='Remove active point')
        remove_point_btn.bind(
            on_press=lambda a: widget.selected_obj.delete_active_point(widget)
        )

        draw_texture_btn = Button(text='Fill texture')
        draw_texture_btn.bind(
            on_press=lambda a: widget.selected_obj.draw_texture(widget)
        )
        object_settings_box.add_widget(add_point_btn)
        object_settings_box.add_widget(change_active_point_btn)
        object_settings_box.add_widget(fill_polygon_btn)
        object_settings_box.add_widget(find_intersection_btn)
        object_settings_box.add_widget(remove_point_btn)
        object_settings_box.add_widget(draw_texture_btn)
