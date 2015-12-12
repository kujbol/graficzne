from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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

        color_count = TextInput(text='Color count')
        color_count.bind(
            text=lambda instance, value: widget.selected_obj.set_color_count(
                value
            )
        )

        cut_colors = CheckBox(active=widget.selected_obj.settings.cut_colors)
        cut_colors.bind(
            active=lambda instance, value: widget.selected_obj.set_color_cut(
                value
            )
        )

        label_cut_colors = Label(
            text='[color=000000]Cut colors[/color]', markup=True
        )
        box_cut_color = BoxLayout(orientation='horizontal')
        box_cut_color.add_widget(label_cut_colors)
        box_cut_color.add_widget(cut_colors)

        shadows = CheckBox(active=widget.selected_obj.settings.shadows)
        shadows.bind(
            active=lambda instance, value: widget.selected_obj.set_shadows(
                value
            )
        )
        shadows_label = Label(
            text='[color=000000]Shadows[/color]', markup=True
        )
        box_shadows = BoxLayout(orientation='horizontal')
        box_shadows.add_widget(shadows_label)
        box_shadows.add_widget(shadows)

        bump_mapping = CheckBox(active=widget.selected_obj.settings.bump_mapping)
        bump_mapping.bind(
            active=lambda instance, value: widget.selected_obj.set_bump_mapping(
                value
            )
        )
        bump_mapping_label = Label(
            text='[color=000000]Bump map[/color]', markup=True
        )
        box_bump_mapping = BoxLayout(orientation='horizontal')
        box_bump_mapping.add_widget(bump_mapping_label)
        box_bump_mapping.add_widget(bump_mapping)

        object_settings_box.add_widget(add_point_btn)
        object_settings_box.add_widget(change_active_point_btn)
        object_settings_box.add_widget(fill_polygon_btn)
        # object_settings_box.add_widget(find_intersection_btn)
        object_settings_box.add_widget(remove_point_btn)
        object_settings_box.add_widget(draw_texture_btn)
        object_settings_box.add_widget(box_cut_color)
        object_settings_box.add_widget(box_shadows)
        object_settings_box.add_widget(box_bump_mapping)
