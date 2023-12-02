import pygame
import pygame_gui
import os
from tkinter import Tk, filedialog  # Import for file dialog

pygame.init()

pygame.display.set_caption('Multi-Screen Application')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill("#3a3b3c")

manager = pygame_gui.UIManager((800, 600))

# Placeholder variables to store user choices
selected_image = None
selected_colors = []
selected_frame_size = None

# Function to create Main Menu (Screen 1)
def create_main_menu():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Main Menu',
                                         manager=manager)
    next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 200, 150, 40),
                                                text='Next >>',
                                                manager=manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'bottom'})
    return next_button

# Placeholder variables to store user choices
selected_image = None
selected_colors = []
selected_frame_size = None
selected_image_folder = None  # New variable to store selected image folder

# Function to create Image Selection (Screen 2)
def create_image_selection():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Select Image',
                                         manager=manager)

    folder_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(100, 150, 400, 30),
                                                       manager=manager)
    
    browse_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(520, 150, 80, 30),
                                                 text='Browse',
                                                 manager=manager)
    
    def on_browse_button_pressed():
        root = Tk()
        root.withdraw()
        selected_folder = filedialog.askdirectory()
        folder_input.set_text(selected_folder)

    browse_button.subscribe(on_browse_button_pressed)

    def on_image_selection(button_text):
        selected_image_folder = folder_input.get_text()
        print(f'Selected Image Folder: {selected_image_folder}')

        # Use the selected folder to list images
        image_list = [f for f in os.listdir(selected_image_folder) if f.endswith(('png', 'jpg', 'jpeg'))]
        print(f'Available Images: {image_list}')

    next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 200, 150, 40),
                                                text='Next >>',
                                                manager=manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'bottom'})
    
    browse_button.subscribe(on_image_selection, 'Next >>')

    return next_button

# Function to create Color Picker (Screen 3)
def create_color_picker():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Color Picker',
                                         manager=manager)

    def on_color_selection(button_text):
        if button_text == 'Add Color':
            if len(selected_colors) < 14:
                selected_colors.append('#FFFFFF')  # Placeholder, you can implement a color picker here
        elif button_text == 'Remove Color':
            if selected_colors:
                selected_colors.pop()

        print(f'Selected Colors: {selected_colors}')

    add_color_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 250, 150, 40),
                                                    text='Add Color',
                                                    manager=manager,
                                                    anchors={'left': 'left',
                                                             'right': 'right',
                                                             'top': 'top',
                                                             'bottom': 'bottom'})
    remove_color_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 300, 150, 40),
                                                       text='Remove Color',
                                                       manager=manager,
                                                       anchors={'left': 'left',
                                                                'right': 'right',
                                                                'top': 'top',
                                                                'bottom': 'bottom'})
    next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 500, 150, 40),
                                                text='Next >>',
                                                manager=manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'bottom'})

    add_color_button.subscribe(on_color_selection, 'Add Color')
    remove_color_button.subscribe(on_color_selection, 'Remove Color')

    return next_button

# Function to create Frame Size Selection (Screen 4)
def create_frame_size_selection():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Select Frame Size',
                                         manager=manager)

    frame_size_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect(100, 200, 150, 30),
                                                           manager=manager)

    def on_frame_size_selection(button_text):
        selected_frame_size = frame_size_input.get_text()
        print(f'Selected Frame Size: {selected_frame_size}')

    next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 500, 150, 40),
                                                text='Next >>',
                                                manager=manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'bottom'})
    next_button.subscribe(on_frame_size_selection, 'Next >>')

    return next_button

# Function to create Image Preview (Screen 5)
def create_image_preview():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Image Preview',
                                         manager=manager)
    next_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 500, 150, 40),
                                                text='Next >>',
                                                manager=manager,
                                                anchors={'left': 'left',
                                                         'right': 'right',
                                                         'top': 'top',
                                                         'bottom': 'bottom'})
    return next_button

# Function to create Thank You (Screen 6)
def create_thank_you():
    label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(100, 100, 200, 50),
                                         text='Thank You!',
                                         manager=manager)
    finish_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(100, 500, 150, 40),
                                                  text='Finish',
                                                  manager=manager,
                                                  anchors={'left': 'left',
                                                           'right': 'right',
                                                           'top': 'top',
                                                           'bottom': 'bottom'})
    return finish_button

# Initial screen
current_screen = create_main_menu()

# Main loop
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == current_screen:
                if current_screen == create_main_menu():
                    current_screen = create_image_selection()
                elif current_screen == create_image_selection():
                    current_screen = create_color_picker()
                elif current_screen == create_color_picker():
                    current_screen = create_frame_size_selection()
                elif current_screen == create_frame_size_selection():
                    current_screen = create_image_preview()
                elif current_screen == create_image_preview():
                    current_screen = create_thank_you()
                elif current_screen == create_thank_you():
                    pygame.quit() 
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
