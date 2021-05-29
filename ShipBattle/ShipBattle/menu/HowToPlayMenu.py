import pygame
from menu.Menu import Menu

class HowToPlayMenu(Menu):
    def __init__(self, nameMenu, nameSprite):
        super().__init__(nameMenu, nameSprite)

    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.dict["button"] == 1:
                    self.mainMenu_loop = False

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

    def main_loop(self):
        while self.mainMenu_loop:
            self._handel_inputs()
            self._draw()
