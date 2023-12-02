import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

class MultiScreenApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multi-Screen GUI")
        self.root.geometry("800x600")

        self.current_screen = 1
        self.num_screens = 6

        self.image_path = None
        self.image_label = None
        
        self.create_widgets()

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
        self.label.config(text="Screen {}".format(self.current_screen))

        if self.current_screen == 1:
            self.next_button.pack(side=tk.RIGHT)
            self.prev_button.pack_forget()  # Hide the Prev button
        elif 1 < self.current_screen < self.num_screens:
            self.next_button.pack(side=tk.RIGHT)
            self.prev_button.pack(side=tk.LEFT)
        elif self.current_screen == self.num_screens:
            self.next_button.pack_forget()  # Hide the Next button
            finish_button = tk.Button(self.root, text="Finish", command=self.finish)
            finish_button.pack(side=tk.RIGHT)

    def create_image_screen(self):
        self.image_label = tk.Label(self.root, text="Select and Load an Image", padx=10, pady=10)
        self.image_label.pack()

        select_button = tk.Button(self.root, text="Select Image", command=self.select_image)
        select_button.pack()

    def select_image(self):
        file_path = filedialog.askopenfilename(title="Select an Image", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])

        if file_path:
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MultiScreenApp(root)
    root.mainloop()