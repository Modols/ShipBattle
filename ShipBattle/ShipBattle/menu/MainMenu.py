import pygame
from shooter.settings import *
from shooter.game import Shooter
from menu.Menu import Menu
from menu.HowToPlayMenu import HowToPlayMenu
from menu.PseudoMenu import PseudoMenu
from menu.SettingsMenu import SettingsMenu
from menu.ScoreMenu import ScoreMenu

class MainMenu(Menu):
    def __init__(self, nameMenu, nameSprite):
        super().__init__(nameMenu, nameSprite)
        self.messages = []
        self.list = []
        self.colorSelected = RED
        self.colorTitle = WHITE
        self.indexTitle = 0
        self.listTitle = [
            ["Jouer", self.colorSelected, SCREEN_WIDTH/2, SCREEN_HEIGHT/2],
            ["Comment Jouer", self.colorTitle, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.72],
            ["Score", self.colorTitle, SCREEN_WIDTH/2, SCREEN_HEIGHT/1.5]
        ]
    
    def main_loop(self):
        while self.mainMenu_loop:
            self._handel_inputs()
            self._draw()

    def _changeColor(self):
        for liste in self.listTitle:
            if (self.listTitle[self.indexTitle] == liste):
                liste[1] = self.colorSelected
            else:
                liste[1] = self.colorTitle

    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.dict["button"] == 0:
                    self._selectMenu(self.listTitle[self.indexTitle][0])

            if event.type == pygame.JOYAXISMOTION:
                if event.dict['axis'] == 1 and round(event.dict['value']) == 1:
                    if self.indexTitle >= 2:
                        self.indexTitle = 0
                    else:
                        self.indexTitle += 1
                    self._changeColor()
            if event.type == pygame.JOYAXISMOTION:
                if event.dict['axis'] == 1 and round(event.dict['value']) == -1:
                    if self.indexTitle == 0:
                        self.indexTitle = 2
                    else:
                        self.indexTitle -= 1
                    self._changeColor()

    def _displayCenterTxt(self):
        for title in self.listTitle:
            txt = self.arial_font.render(title[0], True, title[1])
            txtCenter = txt.get_rect().center
            myTuple = (txt, txtCenter, (title[2], title[3]))
            self.messages.append(myTuple)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self._displayCenterTxt()
        for message in self.messages:
            self.screen.blit(message[0], ((message[2][0]) - message[1][0], message[2][1] - message[1][1]))
        pygame.display.flip()
    
    def _selectMenu(self, nameMenu):
        if nameMenu == "Jouer":
            settings = SettingsMenu("Settings", "parametre_page")
            settings.main_loop()
            settingsListe = settings.getSettingsRequired()
            if settingsListe[0] == True:
                pseudoMenu = PseudoMenu("Pseudo", "pseudo_page")
                pseudoMenu.main_loop()
                pseudo = pseudoMenu.getPseudoStr()
                if pseudo[0] == True:
                    shooter = Shooter(settingsListe[1], settingsListe[2], pseudo[1], pseudo[2])
                    shooter.main_loop()
                
        elif nameMenu == "Comment Jouer":
            howToPlayMenu = HowToPlayMenu("Comment jouer", "instruction_page")
            howToPlayMenu.main_loop()
        elif nameMenu == "Score":
            score = ScoreMenu("Score", "scores_page")
            score.main_loop()
