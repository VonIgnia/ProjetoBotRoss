import tkinter as tk

#Screen 2
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

#Screen 3
from tkinter import colorchooser

def hex_to_rgb(hex):
        return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))
    
    
class MultiScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Screen GUI")
        self.root.geometry("800x600")

        self.current_screen = 1
        self.num_screens = 6

        #Screen 2
        self.image_path = None
        self.selected_image_path = None  # New variable to store the selected image path
        self.image_label = None
        self.select_button = None
        
        #Screen 3
        self.color_list = []
        self.color_list = []  # New list to store selected colors
        self.color_picker_frame = None  # Variable to store color picker frame
        
        self.create_widgets()

    # Multiple screens / General purpose
    def create_widgets(self):
        self.label = tk.Label(self.root, text="Screen {}".format(self.current_screen), padx=10, pady=10)
        self.label.pack()

        self.next_button = tk.Button(self.root, text="Next", command=self.next_screen)
        self.next_button.pack(side=tk.RIGHT)

        self.prev_button = tk.Button(self.root, text="Prev", command=self.prev_screen)
        self.prev_button.pack(side=tk.LEFT)
        self.prev_button.pack_forget()  # Initially hide the Prev button

    def next_screen(self):
        self.current_screen += 1

        if self.current_screen <= self.num_screens:
            self.update_screen()
        else:
            self.finish()

    def prev_screen(self):
        self.current_screen -= 1
        self.update_screen()

    def finish(self):
        result = messagebox.askyesno("Finish", "Do you want to close the app?")
        if result:
            self.root.destroy()
            # Add your remaining code to execute after the GUI is closed here

    def update_screen(self):
        switch_dict = {
            1: self.screen_1,
            2: self.screen_2,
            3: self.screen_3,
            4: self.screen_4,
            5: self.screen_5,
            6: self.screen_6
        }

        screen_function = switch_dict.get(self.current_screen, None)
        if screen_function:
            screen_function()

    def screen_1(self):
        self.label.config(text="Screen 1")
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button.pack_forget()  # Hide the Prev button
        self.destroy_image_widgets()

    def screen_2(self):
        self.label.config(text="Screen 2")
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button.pack(side=tk.LEFT)
        self.destroy_color_picker_frame()

        # Check if a selected image path exists and load the image
        if self.selected_image_path:
            self.create_image_screen()
            self.load_and_display_image(self.selected_image_path)
        else:
            self.create_image_screen()

    def screen_3(self):
        self.destroy_image_widgets()
        self.label.config(text="Screen 3")
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button.pack(side=tk.LEFT)

        if self.color_picker_frame is None:
            self.create_color_picker_screen()  # Create color picker interface

    def screen_4(self):
        # Add functionality for Screen 4
        self.label.config(text="Screen 4")
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button.pack(side=tk.LEFT)
        self.destroy_image_widgets()
        self.destroy_color_picker_frame()

    def screen_5(self):
        # Add functionality for Screen 5
        self.label.config(text="Screen 5")
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button.pack(side=tk.LEFT)
        self.destroy_image_widgets()

    def screen_6(self):
        self.label.config(text="Screen 6")
        self.next_button.pack_forget()  # Hide the Next button
        finish_button = tk.Button(self.root, text="Finish", command=self.finish)
        finish_button.pack(side=tk.RIGHT)
        self.destroy_image_widgets()

# Screen 2 Functions
    def create_image_screen(self):
        #if self.image_label is None:
        self.image_label = tk.Label(self.root, text="Select and Load an Image", padx=10, pady=10)
        self.image_label.pack()

        #if self.select_button is None:
        self.select_button = tk.Button(self.root, text="Select Image", command=self.select_image)
        self.select_button.pack()

        # Check if a selected image path exists and load the image
        if self.selected_image_path:
            self.load_and_display_image(self.selected_image_path)

    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
            self.selected_image_path = file_path  # Store the selected image path
            self.load_and_display_image(file_path)

    def load_and_display_image(self, file_path):
        try:
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)

            if self.image_label is not None:
                self.image_label.destroy()

            self.image_label = tk.Label(self.root, image=photo)
            self.image_label.image = photo
            self.image_label.pack()

            self.image_path = file_path

        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    def destroy_image_widgets(self):
        if self.image_label:
            self.image_label.destroy()
        if self.select_button:
            self.select_button.destroy()

# Screen 3 Functions
    def create_color_picker_screen(self):
        self.color_picker_frame = tk.Frame(self.root)
        self.color_picker_frame.pack()

        color_picker_label = tk.Label(self.color_picker_frame, text="Color Picker", padx=10, pady=10)
        color_picker_label.pack()

        color_picker_button = tk.Button(self.color_picker_frame, text="Pick a Color", command=self.pick_color)
        color_picker_button.pack()

        # Create squares to display selected colors
        for color in self.color_list:
            color_square = tk.Label(self.color_picker_frame, text="     ", bg=color, padx=5, pady=5)
            color_square.pack()
    
    

    def pick_color(self):
        color = colorchooser.askcolor()[1]
        if color:
            self.color_list.append(color)

            # Update the color squares
            self.update_color_squares()
            print(hex_to_rgb(color))
            
    def update_color_squares(self):
        # Destroy existing color squares
        for widget in self.color_picker_frame.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget("bg") in self.color_list:
                widget.destroy()

        # Create new color squares
        for color in self.color_list:
            color_square = tk.Label(self.color_picker_frame, text="     ", bg=color, padx=5, pady=5)
            color_square.pack()
    
    def destroy_color_picker_frame(self):
        # Unpack and destroy the color picker frame
        if self.color_picker_frame:
            self.color_picker_frame.pack_forget()
            self.color_picker_frame.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScreenApp(root)
    root.mainloop()
