import pygame
from menu.Menu import Menu
from menu.ListSetting import ListSetting
from shooter.bdd import BDD
from shooter.settings import *
from shooter.utils import load_sprite

class SettingsMenu(Menu):
    def __init__(self, nameMenu, nameSprite):
        self.settings_loop = True
        self.settingsListName = SETTINGS_LIST_NAME
        self.indexPlayer1 = 0
        self.indexPlayer2 = 0

        self.displayBoat = []
        self.displayText = []
        self.bdd = BDD()
        self.gameCanStart = False

        self.listeSettings2 = self.bdd.selectSetting('player2')
        self.listeSettings1 = self.bdd.selectSetting('player1')

        self.listeSettingsPlayer1 = ListSetting(self.listeSettings1, self.settingsListName)
        self.listeSettingsPlayer2 = ListSetting(self.listeSettings2, self.settingsListName)

        super().__init__(nameMenu, nameSprite)
        self.arial_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_SCORE)

    def main_loop(self):
        while self.settings_loop:
            self._handel_inputs()
            self._draw()
            self._checkSatusPlayer(self.listeSettingsPlayer1.listeSettingsAndName, self.listeSettingsPlayer2.listeSettingsAndName)
            
    def _checkSatusPlayer(self, listeP1, listeP2):
        if listeP1[7][0] == "READY" and listeP2[7][0] == "READY":
            self.settings_loop = False
            self.gameCanStart = True
            self.bdd.updateSettings("player1", self.listeSettingsPlayer1.formatListeForBddUpdate())
            self.bdd.updateSettings("player2", self.listeSettingsPlayer2.formatListeForBddUpdate())
        
    def getSettingsRequired(self):
        boatPlayer1 = self.listeSettingsPlayer1.listeSettingsAndName[0][0]
        boatPlayer2 = self.listeSettingsPlayer2.listeSettingsAndName[0][0]
        return [self.gameCanStart, boatPlayer1, boatPlayer2]

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        
        self._createTxtTupleToList(self.indexPlayer1, self.listeSettingsPlayer1.listeSettingsAndName, SCREEN_WIDTH* 1.80/5, 300)
        self._createTxtTupleToList(self.indexPlayer2, self.listeSettingsPlayer2.listeSettingsAndName, SCREEN_WIDTH* 4.25/5, 300)
        self._createPngBoatAndAddToList(self.listeSettingsPlayer1.listeSettingsAndName[0][0], SCREEN_WIDTH * 0.75/5, SCREEN_HEIGHT/2)
        self._createPngBoatAndAddToList(self.listeSettingsPlayer2.listeSettingsAndName[0][0], SCREEN_WIDTH * 3.25/5, SCREEN_HEIGHT/2)
        
        for txt in self.displayText:
            self.screen.blit(txt[0], ((txt[2][0]) - txt[1][0], txt[2][1] - txt[1][1]))
        for boat in self.displayBoat:
            self.screen.blit(boat[0], ((boat[2][0]) - boat[1][0], boat[2][1] - boat[1][1]))

        pygame.display.flip()
        self.displayText = []
        self.displayBoat = []

    def _handel_inputs(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.dict["button"] == 1 :
                    self.settings_loop = False
                if event.dict["button"] == 0 and event.dict["instance_id"] == 0 :
                    self.listeSettingsPlayer1.listeSettingsAndName[7][0] = super().changeReadyStatus(self.listeSettingsPlayer1.listeSettingsAndName[7][0], True)
                    
                if event.dict["button"] == 0 and event.dict["instance_id"] == 1 :
                    self.listeSettingsPlayer2.listeSettingsAndName[7][0] = super().changeReadyStatus(self.listeSettingsPlayer2.listeSettingsAndName[7][0], True)
                  
            if event.type == pygame.JOYAXISMOTION:
                self.indexPlayer1, self.listeSettingsPlayer1.listeSettingsAndName = self._inputsShortCut(event, self.indexPlayer1, self.listeSettingsPlayer1.listeSettingsAndName, 0)
                self.indexPlayer2, self.listeSettingsPlayer2.listeSettingsAndName = self._inputsShortCut(event, self.indexPlayer2, self.listeSettingsPlayer2.listeSettingsAndName, 1)

    def _createTxtTupleToList(self, colorIdx, liste, surfaceX, surfaceY):
        for idx, setting in enumerate(liste):
            if idx == colorIdx:
                color = RED
            else:
                color = WHITE
            if idx != 0:
                strTxt = str(setting[0])
                txt = self.arial_font.render(strTxt, True, color)
                txtCenter = txt.get_rect().center
                surfaceY = surfaceY + 80
                myTuple = (txt, txtCenter, (surfaceX, surfaceY))
                self.displayText.append(myTuple)

    def _createPngBoatAndAddToList(self, boatNumber, surfaceX, surfaceY):
        boat = load_sprite(f"ship ({boatNumber})")
        boatCenter = boat.get_rect().center 
        myTuple = (boat, boatCenter, (surfaceX, surfaceY))
        self.displayBoat.append(myTuple)

    def _inputsShortCut(self, event, indexPlayer, listeSettingsPlayer, instance_id):
        # handel un deplacement vers le bas
        if event.dict['axis'] == 1 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance_id:
            if indexPlayer == 7:
                indexPlayer = 7
            else:
                indexPlayer += 1
        # handel un deplacement vers le haut
        if event.dict['axis'] == 1 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance_id:
            if indexPlayer == 0:
                indexPlayer = 0
            else:
                indexPlayer -= 1
        # handel un deplacement vers la droite
        if event.dict['axis'] == 0 and round(event.dict['value']) == 1 and event.dict['instance_id'] == instance_id:
            if indexPlayer == 7: 
                pass
            elif indexPlayer == 0:
                if listeSettingsPlayer[indexPlayer][0] == 6:
                    listeSettingsPlayer[indexPlayer][0] = 3
                else :
                    listeSettingsPlayer[indexPlayer][0] += 1
            else:
                if type(listeSettingsPlayer[indexPlayer][0]) is float :
                    listeSettingsPlayer[indexPlayer][0] = round(listeSettingsPlayer[indexPlayer][0] +0.2,1) 
                else:
                    listeSettingsPlayer[indexPlayer][0] += 1
        # handel un deplacement vers la gauche
        if event.dict['axis'] == 0 and round(event.dict['value']) == -1 and event.dict['instance_id'] == instance_id:
            if indexPlayer == 7:
                pass
            elif indexPlayer == 0:
                if listeSettingsPlayer[indexPlayer][0] == 3:
                    listeSettingsPlayer[indexPlayer][0] = 6
                else :
                    listeSettingsPlayer[indexPlayer][0] -= 1
            else:
                if listeSettingsPlayer[indexPlayer][0] > 0.2:
                    if type(listeSettingsPlayer[indexPlayer][0]) is float :
                        listeSettingsPlayer[indexPlayer][0] = round(listeSettingsPlayer[indexPlayer][0] -0.2,1) 
                    else:
                        if listeSettingsPlayer[indexPlayer][0] > 1:
                            listeSettingsPlayer[indexPlayer][0] -= 1
        return indexPlayer, listeSettingsPlayer
