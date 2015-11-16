from kivy.graphics import Color

from objects.line import Line


# interface for SettingsWidgetClass
class BasicSettingWidgetClass(object):
    setting_class = None
    obj = None

    def remove_settings(self, widget):
        widget.on_press_button(Line)
        object_settings_box = widget.additional_settings_box
        object_settings_box.clear_widgets()


class BasicSettings(object):
    color_box = None
    anty_aliasing = None
    thickness = None


def get_widget_by_name(widget, name):
    return widget.ids[name]


def load_settings(widget, obj):
    box = widget.object_settings_box

    color_edit = get_widget_by_name(widget, 'color_textbox')
    color_edit.text = '{} {} {}'.format(
        obj.settings.color.r, obj.settings.color.g,
        obj.settings.color.b
    )

    anty_aliasing_check = get_widget_by_name(widget, 'anty_aliasing_checkbox')
    anty_aliasing_check.active = obj.settings.anty_aliasing

    thickness_edit = get_widget_by_name(widget, 'thickness_textbox')
    thickness_edit.text = str(obj.settings.thickness)

    widget.saved_color = widget.selected_obj.settings.color
    widget.selected_obj.settings.color = Color(.9, 0, .1)

    load_settings_widgets(widget, obj)


def load_settings_widgets(widget, obj):
    for settings_widget in widget.settings_widgets:
        if isinstance(obj, settings_widget.setting_class):
            settings_widget.add_settings(widget)
            break
    else:
        widget.additional_settings_box.clear_widgets()
