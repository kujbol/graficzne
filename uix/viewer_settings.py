from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

from uix.basics import BasicSettingWidgetClass
from objects.viewer import Viewer


class ViewerSettingsWidget(BasicSettingWidgetClass):
    setting_class = Viewer
    requirements = []

    def add_settings(self, widget):
        self.remove_settings(widget)

        object_settings_box = widget.additional_settings_box

        height_edit = TextInput(text='height')
        height_edit.bind(
            text=lambda instance, value: widget.selected_obj.change_height(
                value
            )
        )

        object_settings_box.add_widget(height_edit)
