import pygame
from shooter.settings import *
from shooter.utils import load_sprite

class Menu:
    def __init__(self, nameMenu, nameSprite):
        pygame.init()
        self._init_joysticks()
        self.mainMenu_loop = True
        self.arial_font = pygame.font.SysFont(FONT_FAMILY_MENU, FONT_SIZE_MENU)
        self._display_Menu(nameMenu, nameSprite)

    def _display_Menu(self, nameMenu, nameSprite):
        pygame.display.set_caption(nameMenu)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_sprite(nameSprite)
        
    def _init_joysticks(self):
        self.joystick0 = pygame.joystick.Joystick(0)
        self.joystick0.init()
        self.joystick1 = pygame.joystick.Joystick(1)
        self.joystick1.init()

    def changeReadyStatus(self, settingsPlayer, settings = False):
        if settings:
            if settingsPlayer == "NOT READY":
                settingsPlayer = "READY"
            else : 
                settingsPlayer = "NOT READY"
        else:
            if settingsPlayer == True:
                settingsPlayer = False
            else:
                settingsPlayer = True
        return settingsPlayer


