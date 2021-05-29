import pygame
from menu.Menu import Menu
from shooter.bdd import BDD
from shooter.settings import *


class ScoreMenu(Menu):
    def __init__(self, nameMenu, nameSprite):
        super().__init__(nameMenu, nameSprite)
        self.arial_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SCORE)
        bdd = BDD()
        self.scores = []
        self.listScore = bdd.select("SELECT * FROM SCORE order by SCORE.SCORE DESC limit 10")
        self._dispay_Centered_Score(RED, SCREEN_WIDTH/2, 250)

    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.dict["button"] == 1:
                    self.mainMenu_loop = False

    def _dispay_Centered_Score(self, color, surfaceX, surfaceY):
        for idx, score in enumerate(self.listScore):
            idx += 1
            str_txt = f"{idx}. {score.pseudo} | Score : {score.score}"
            txt = self.arial_font.render(str_txt, True, color)
            txtCenter = txt.get_rect().center
            surfaceY = surfaceY + 63
            myTuple = (txt, txtCenter, (surfaceX, surfaceY))
            self.scores.append(myTuple)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for score in self.scores:
            self.screen.blit(score[0], ((score[2][0]) - score[1][0], score[2][1] - score[1][1]))
        pygame.display.flip()

    def main_loop(self):
        while self.mainMenu_loop:
            self._handel_inputs()
            self._draw()
