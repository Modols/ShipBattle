import pygame
from menu.ExceptionMenu import ExceptionMenu
from menu.MainMenu import MainMenu

if __name__ == "__main__":
    try:
        menu = MainMenu("MainMenu", "Main_menu")
        menu.main_loop()
    except pygame.error as e:
        exceptionMenu = ExceptionMenu("Exception", "water-finals", str(e))
        exceptionMenu.main_loop()