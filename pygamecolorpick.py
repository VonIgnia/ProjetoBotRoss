#UI elements
import pygame
import sys
import pygame_gui

from pygame_gui.elements import UIButton
from pygame_gui.windows import UIColourPickerDialog

#opencv image processing elements
import colorsys
import cv2

def ConvertColorRGBtoHSV(color_in):
    # Normalize
    (r, g, b) = (color_in[0] / 255, color_in[1] / 255, color_in[2] / 255)
    # Convert to HSV
    (h, s, v) = colorsys.rgb_to_hsv(r, g, b)
    # Expand HSV range
    (h, s, v) = (int(h * 179), int(s * 255), int(v * 255))
    print('HSV : ', h, s, v)
    return [h,s,v]
    

pygame.init()

pygame.display.set_caption('Bot Ross v2 GUI')
SCREEN = pygame.display.set_mode((800, 600))

ui_manager = pygame_gui.UIManager((800, 600))
background = pygame.Surface((800, 600))
background.fill("#3a3b3c")


colour_picker_button = UIButton(relative_rect=pygame.Rect(-600, -60, 150, 30),
                                text='Pick Colour',
                                manager=ui_manager,
                                anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})

next_page_button = UIButton(relative_rect=pygame.Rect(-180, -60, 150, 30),
                                text='Next',
                                manager=ui_manager,
                                anchors={'left': 'right',
                                        'right': 'right',
                                        'top': 'bottom',
                                        'bottom': 'bottom'})
colour_picker = None


picked_colours_list = []
picked_colours_list_hsv = []                                   
current_colour = pygame.Color(0, 0, 0)
picked_colour_surface = pygame.Surface((400, 400))
picked_colour_surface.fill(current_colour)


clock = pygame.time.Clock()

while True:
    time_delta = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == colour_picker_button:
            colour_picker = UIColourPickerDialog(pygame.Rect(160, 50, 420, 400),
                                                ui_manager,
                                                window_title="Selecione as cores disponíveis",
                                                initial_colour=current_colour)
            colour_picker_button.disable()
            
        if event.type == pygame_gui.UI_COLOUR_PICKER_COLOUR_PICKED:
            current_colour = event.colour
            picked_colour_surface.fill(current_colour)
            picked_colours_list.append(current_colour)
            current_colour_hsv = ConvertColorRGBtoHSV(current_colour)
            picked_colours_list_hsv.append(current_colour_hsv)
            
        if event.type == pygame_gui.UI_WINDOW_CLOSE:
            colour_picker_button.enable()
            colour_picker = None
        
        ui_manager.process_events(event)
        
    ui_manager.update(time_delta)

    SCREEN.blit(background, (0, 0))
    SCREEN.blit(picked_colour_surface, (200, 100))

    ui_manager.draw_ui(SCREEN)

    for color in picked_colours_list:
        colour_surface = pygame.Surface((100, 100))
        colour_surface.fill(color)

    pygame.display.update()