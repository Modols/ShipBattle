import pygame
from shooter.settings import *
from shooter.utils import load_sprite

class ExceptionMenu:
    def __init__(self, nameMenu, nameSprite, exception):
        self.exceptionMenu_loop = True
        self.exception = exception
        print(self.exception)
        self.messages = []
        self.arial_font = pygame.font.SysFont(FONT_FAMILY_MENU, FONT_SIZE_MENU)
        self._display_Menu(nameMenu, nameSprite)

    def _display_Menu(self, nameMenu, nameSprite):
        pygame.display.set_caption(nameMenu)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_sprite(nameSprite)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self._displayCenterTxt(self.exception)
        for message in self.messages:
            self.screen.blit(message[0], ((message[2][0]) - message[1][0], message[2][1] - message[1][1]))
        pygame.display.flip()

    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

    def _displayCenterTxt(self, exception):
        txt = self.arial_font.render(exception, True, RED)
        txtCenter = txt.get_rect().center
        myTuple = (txt, txtCenter, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.messages.append(myTuple)

    def main_loop(self):
        while self.exceptionMenu_loop:
            self._draw()
            self._handel_inputs()