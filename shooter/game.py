import pygame, datetime, time 
from shooter.score import Score
from shooter.settings import *
from shooter.player import Player
from shooter.utils import load_sprite
from shooter.bdd import BDD
from shooter.explosion import Explosion


class Shooter:
    def __init__(self, boatNumber1, boatNumber2, pseudo1, pseudo2):
        self._init_pygame()
        self.bdd = BDD()
        
        self.tupleSettingsP1 = self.bdd.selectSetting("player1")
        self.tupleSettingsP2 = self.bdd.selectSetting("player2")

        self.playing = PLAYING
        self.LOOP_GAME = LOOP_GAME
        self.endGame = LOOP_END_GAME
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = load_sprite("background")
        self.clock = pygame.time.Clock()
        self.timeGameStart = datetime.datetime.utcfromtimestamp(time.time())

        self.player2 = Player(PLAYER1_POSITION, 1, pseudo1, self.tupleSettingsP1, boatNumber1, "cannonBall")
        self.player1 = Player(PLAYER2_POSITION, 0, pseudo2, self.tupleSettingsP2, boatNumber2, "cannonBall")
        self.players = []
        self.players.extend([self.player1, self.player2])

        self.arial_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        self.messages = []

        self.explosions = []
        self.pirates = []

        self._create_message(self.player2.pseudo, (10, 10), RED)
        self._create_message(self.player1.pseudo, (SCREEN_WIDTH - 160, 10), RED)
        
    def main_loop(self):
        while self.LOOP_GAME:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Shooter")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if self.playing == "playing":
                if event.type == pygame.JOYBUTTONDOWN:
                    if (event.dict["instance_id"] == 1 and event.dict["button"] == 0):
                        self.player1.canShoot()
                    elif (event.dict["instance_id"] == 0 and event.dict["button"] == 0):
                        self.player2.canShoot()

        if self.playing == "playing":
            for player in self.players:
                if (round(player.joystick.get_axis(0)) ==  -1):
                    player.rotate(-1)
                if (round(player.joystick.get_axis(0)) ==  1):
                    player.rotate(1)
                if (round(player.joystick.get_axis(1)) ==  -1):
                    player.accelerate()
                if (round(player.joystick.get_axis(1)) ==  1):
                    player.deceleration()

    def _process_game_logic(self):
        if(len(self.players) == 2):
            for idx, player in enumerate(self.players):
                player.move(self.screen)
                if player == self.player1 :
                    next_player = self.player2
                else:
                    next_player = self.player1

                for bullet in player.bullets:
                    bullet.move()
                    if not self.screen.get_rect().collidepoint(bullet.position):
                        player.bullets.remove(bullet)
                    if (bullet.collides_with(next_player)) :
                        explosion = Explosion(bullet.position)
                        self.explosions.append(explosion)
                        player.bullets.remove(bullet)
                        del bullet
                        if((next_player.health - player.power_shooting) <= 0 ):
                            next_player.updateHealth(-player.power_shooting)
                            self.players.remove(next_player)
                            del next_player
                        else:
                            next_player.changeSprite(self.pirates)
                            next_player.updateHealth(-player.power_shooting)
        else:
            self.playing = "freeze"
            self._game_over(self.players[0])
            while self.endGame:
                self._draw()
                for event in pygame.event.get():
                    if event.type == pygame.JOYBUTTONDOWN:
                        if (event.dict["button"] == 1):
                            self.LOOP_GAME = False
                            self.endGame = False
        
    def _game_over(self, player):
        player.score = self._calculScore(player)
        id = self.bdd.getNextId("SCORE")
        tmpScore = Score([id, player.pseudo, player.score])
        self.bdd.insertScore([tmpScore.pseudo, tmpScore.score])
        position = self._getPosition(tmpScore)
        txt = f'{player.pseudo} à gagné la partie avec {player.score}'
        classement = ("er" if position == 1 else "ème") 
        txt2 = f'Vous êtes {position}{classement} dans le classement'
        self.messages = []

        self.arial_font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE_WIN)
        self._create_message(txt, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2), ORANGE, True)
        self._create_message(txt2, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + FONT_SIZE_WIN + 20), ORANGE, True)

    def _calculScore(self, player):
        if player == self.player1:
            playerWin = player
            playerLose = self.bdd.selectSetting("player1")
        else:
            playerWin = player
            playerLose = self.bdd.selectSetting("player2")

        gameTime = datetime.timedelta.total_seconds(datetime.datetime.utcfromtimestamp(time.time()) - self.timeGameStart)
        deltaManeuvrability = (round(playerWin.maneuverability - playerLose[1],1) if round(playerWin.maneuverability - playerLose[1],1) > 0 else round(abs(playerWin.maneuverability - playerLose[1]),1) *5)
        deltaAcceleration = (round(playerWin.acceleration - playerLose[2],1) if round(playerWin.acceleration - playerLose[2],1) > 0 else round(abs(playerWin.acceleration - playerLose[2]),1) *5)
        deltaBullet_speed = (round(playerWin.bullet_speed - playerLose[3],1) if round(playerWin.bullet_speed - playerLose[3],1) > 0 else round(abs(playerWin.bullet_speed - playerLose[3]),1) *5)
        deltaPtsHealth = (playerWin.maxHealth - playerLose[4] if playerWin.maxHealth - playerLose[4] > 0 else abs(playerWin.maxHealth - playerLose[4]) *2)
        deltaDelay_shoot = (round(playerWin.delay_shoot - playerLose[5],1) if round(playerWin.delay_shoot - playerLose[5],1) > 0 else round(abs(playerWin.delay_shoot - playerLose[5]),1) *5)
        deltaPower_shooting = (playerWin.power_shooting - playerLose[6] if playerWin.power_shooting - playerLose[6] > 0 else abs(playerWin.power_shooting - playerLose[6]) *2)
        
        endScore = gameTime + deltaManeuvrability + deltaAcceleration + deltaBullet_speed + deltaPtsHealth + deltaDelay_shoot + deltaPower_shooting
        return (round(endScore)* 50)

    def _getPosition(self, tmpScore):
        listScore = self.bdd.select("SELECT * FROM SCORE order by SCORE.SCORE DESC ")
        for idx, score in enumerate(listScore):
            idx += 1
            if tmpScore.id == score.id:
                return idx

    def _create_message(self, message, message_position, color, isGameOver = False):
        txt = self.arial_font.render(message, True, color)
        txtRect = txt.get_rect().center
        myTuple = (txt, message_position)
        if isGameOver:
            new_position = (message_position[0] - txtRect[0] , message_position[1] - txtRect[1])
            myTuple = (txt, new_position)

        self.messages.append(myTuple)

    def _draw(self):
        self.screen.blit(self.background, (0, 0))
        for pirate in self.pirates:
            pirate.draw(self.screen)
        for player in self.players:
            player.draw(self.screen)
            for bullet in player.bullets:
                bullet.draw(self.screen)
        for message in self.messages:
            self.screen.blit(message[0], message[1])
        for explosion in self.explosions:
            if (explosion.checkTimer()):
                self.explosions.remove(explosion)
                del explosion
            else:
                explosion.draw(self.screen)
        
        pygame.display.flip()
        self.clock.tick(60)