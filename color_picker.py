
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

        self.layout = GridLayout(cols=2)

        color_picker = ColorPicker()
        self.layout.add_widget(color_picker)
        
        color_scrollview = ScrollView(size=(400, 300), size_hint=(None, None))
        color_layout = BoxLayout(orientation="vertical", spacing=5, size_hint_y=None)
        color_scrollview.add_widget(color_layout)

        self.color_labels = []

        for _ in range(14):
            color_label = Label(text="", size_hint_y=None, height=30)
            color_layout.add_widget(color_label)
            self.color_labels.append(color_label)
        
        self.layout.add_widget(color_scrollview)
        
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
"""
        color_scrollview = ScrollView(size=(400, 300), size_hint=(None, None))
        color_layout = GridLayout(orientation="vertical", spacing=5, size_hint_y=None)
        color_scrollview.add_widget(color_layout)

        self.color_labels = []

        for _ in range(14):
            color_label = Label(text="", size_hint_y=None, height=30)
            color_layout.add_widget(color_label)
            self.color_labels.append(color_label)

        self.layout.add_widget(color_scrollview)

        pick_button = Button(text="Pick Color", on_press=self.pick_color)
        self.layout.add_widget(pick_button)

        remove_button = Button(text="Remove Selected", on_press=self.remove_selected)
        self.layout.add_widget(remove_button)

        show_button = Button(text="Show Selected", on_press=self.show_selected)
        self.layout.add_widget(show_button)

        return self.layout
    
    def pick_color(self, instance):
        color_picker = ColorPicker()
        color_picker.bind(color=self.on_color_picker_change)


    def on_color_picker_change(self, instance, value):
        if len(self.selected_colors) < 14 and value not in self.selected_colors:
            self.selected_colors.append(value)
            self.update_color_labels()

    def remove_selected(self, instance):
        if self.selected_colors:
            self.selected_colors.pop()
            self.update_color_labels()

    def show_selected(self, instance):
        if self.selected_colors:
            color_str = ", ".join(self.selected_colors)
        else:
            color_str = "No colors selected."

        self.root.get_screen("main").children[0].text = f"Selected Colors: {color_str}"

    def update_color_labels(self):
        for i, color_label in enumerate(self.color_labels):
            if i < len(self.selected_colors):
                color_label.text = f"[color={self.selected_colors[i]}]██[/color]"
            else:
                color_label.text = ""
"""

if __name__ == "__main__":
    ColorPickerApp().run()