
from kivy.app import App

from kivy.uix.colorpicker import ColorPicker
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView


class ColorPickerApp(App):
    def build(self):
        self.selected_colors = []

        self.layout = GridLayout(cols=2, spacing=10, padding=10)

        # Column 1: ColorPicker
        color_picker = ColorPicker()
        color_picker.bind(color=self.on_color_picker_change)
        self.layout.add_widget(color_picker)

        # Column 2: Array of Selected Colors
        color_layout = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.color_scrollview = ScrollView(size_hint=(None, None), size=(200, 300))
        self.color_scrollview.add_widget(color_layout)
        
        
        self.color_labels = []

        for _ in range(14):
            color_label = Label(text="", size_hint_y=None, height=30)
            color_layout.add_widget(color_label)
            self.color_labels.append(color_label)
        
        self.layout.add_widget(self.color_scrollview)
        
        pick_button = Button(text="Pick Color", on_press=self.pick_color)
        self.layout.add_widget(pick_button)
        
        remove_button = Button(text="Remove Selected", on_press=self.remove_selected)
        self.layout.add_widget(remove_button)
        
        return self.layout
    
    def pick_color(self, instance):
        color_picker = ColorPicker()
        color_picker.bind(color=self.on_color_picker_change)
        
    def on_color_picker_change(self, instance, value):
        if len(self.selected_colors) < 14 and value not in self.selected_colors:
            self.selected_colors.append(value)
            self.update_color_labels()

    def update_color_labels(self):
        for i, color_label in enumerate(self.color_labels):
            if i < len(self.selected_colors):
                color_label.text = f"[color={self.selected_colors[i]}]██[/color]"
            else:
                color_label.text = ""
    
    def remove_selected(self, instance):
        if self.selected_colors:
            self.selected_colors.pop()
            self.update_color_labels()

if __name__ == "__main__":
    ColorPickerApp().run()