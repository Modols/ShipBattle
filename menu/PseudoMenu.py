import pygame, string
from menu.Menu import Menu
from shooter.settings import *

class PseudoMenu(Menu):
    def __init__(self, nameMenu, nameSprite):
        super().__init__(nameMenu, nameSprite)
        self.arial_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_PSEUDO)
        self.arial_font2 = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SCORE)
        self.alphabetList = list(string.ascii_uppercase)
        self.lettersP1 = [0,0,0,0]
        self.idxP1 = 0
        self.lettersP2 = [0,0,0,0]
        self.idxP2 = 0
        self.lettersListe = [self.lettersP1, self.lettersP2]
        self.displayLetters = []
        self.displayStatus = []
        self.player1Ready = False
        self.player2Ready = False
        self.pseudo_loop = True
        self.gameCanStart = False

    def _displayCenterTxt(self, surfaceX, surfaceY):
        for idx, letters in enumerate(self.lettersListe):
            if idx == 0 :
                playerIdx = self.idxP1
            elif idx == 1 :
                surfaceX = SCREEN_WIDTH * 2/3
                playerIdx = self.idxP2
            for idx2, letterIdx in enumerate(letters):
                if idx2 == playerIdx:
                    color = RED
                else :
                    color = WHITE

                txt = self.arial_font.render(self.alphabetList[letterIdx], True, color)
                txtCenter = txt.get_rect().center
                surfaceX +=  65
                myTuple = (txt, txtCenter, (surfaceX, surfaceY))
                self.displayLetters.append(myTuple)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        self._displayCenterTxt(SCREEN_WIDTH*1/6, SCREEN_HEIGHT/2)
        for letter in self.displayLetters:
            self.screen.blit(letter[0], ((letter[2][0]) - letter[1][0], letter[2][1] - letter[1][1]))
        self._displayCenterStatus()
        for statu in self.displayStatus:
            self.screen.blit(statu[0], ((statu[2][0]) - statu[1][0], statu[2][1] - statu[1][1]))
        
        pygame.display.flip()
        self.displayLetters = []
        self.displayStatus = []

    def _displayCenterStatus(self):
        player1 = ("READY" if self.player1Ready == True else "NOT READY")
        player2 = ("READY" if self.player2Ready == True else "NOT READY")
        players = [player1, player2]
        for idx, player in enumerate(players):
            
            txt = self.arial_font2.render(player, True, WHITE)
            txtCenter = txt.get_rect().center
            
            surfaceX = (SCREEN_WIDTH*1/4 if idx == 0 else SCREEN_WIDTH * 3/4) 
            myTuple = (txt, txtCenter, (surfaceX, SCREEN_HEIGHT*2/3))
            self.displayStatus.append(myTuple)


    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.JOYBUTTONDOWN:
                if event.dict["button"] == 1:
                    self.pseudo_loop = False
                if event.dict["button"] == 0 and event.dict["instance_id"] == 0:
                    self.player1Ready = super().changeReadyStatus(self.player1Ready)
                if event.dict["button"] == 0 and event.dict["instance_id"] == 1:
                    self.player2Ready = super().changeReadyStatus(self.player2Ready)

            if event.type == pygame.JOYAXISMOTION:
                self.idxP1, self.lettersP1 = self._inputsShortCut(event, self.idxP1, self.lettersP1, 0)
                self.idxP2, self.lettersP2 = self._inputsShortCut(event, self.idxP2, self.lettersP2, 1)
   
    def _formatePseudoListe(self):
        liste = []
        for listeLetter in self.lettersListe:
            tmpListe = []
            for letter in listeLetter:
                tmpLetter = self.alphabetList[letter]
                tmpListe.append(tmpLetter)
            liste.append(tmpListe)
        return liste

    def _checkSatusPlayers(self):
        if self.player1Ready == True and self.player2Ready == True:
            self.pseudo_loop = False
            self.gameCanStart = True

    def getPseudoStr(self):
        forma = self._formatePseudoListe()
        pseudo1 = forma[0]
        pseudo1 = "".join(pseudo1)
        pseudo2 = forma[1]
        pseudo2 = "".join(pseudo2)
        return [self.gameCanStart, pseudo1, pseudo2]

    def _inputsShortCut(self, event, idxPlayer, listeLetter, instance_id):
        # handel un deplacement vers le bas
        if event.dict['axis'] == 1 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance_id:
            idxLetter = listeLetter[idxPlayer]
            if idxLetter == 0:
                idxLetter = 25
            else :
                idxLetter -= 1
            listeLetter[idxPlayer] = idxLetter
        # handel un deplacement vers le haut
        if event.dict['axis'] == 1 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance_id:
            idxLetter = listeLetter[idxPlayer]
            if idxLetter == 25:
                idxLetter = 0
            else :
                idxLetter += 1
            listeLetter[idxPlayer] = idxLetter
        # handel un deplacement vers la droite
        if event.dict['axis'] == 0 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance_id:
            if idxPlayer == 3:
                idxPlayer = 0
            else:
                idxPlayer += 1
        # handel un deplacement vers la gauche
        if event.dict['axis'] == 0 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance_id:
            if idxPlayer == 0:
                idxPlayer = 3
            else:
                idxPlayer -= 1
        return idxPlayer, listeLetter

    def main_loop(self):
        while self.pseudo_loop:
            self._handel_inputs()
            self._draw()
            self._checkSatusPlayers()
