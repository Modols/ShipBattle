from pygame.math import Vector2
# screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1920, 1080

# game
LOOP_GAME = True
PLAYING = "playing"
LOOP_END_GAME = True

# player
UP = Vector2(0, -1)
PLAYER_WIDTH = 63
PLAYER_HEIGHT = 113

# to reset db
MANEUVERABILITY = 3
ACCELERATION = 2.5
BULLET_SPEED = 7
HEALTH = 5
DELAY_SHOOT = 0.75
POWER_SHOOTING = 1

# player1 position
PLAYER1_POSITION = ( (100 + PLAYER_WIDTH) , SCREEN_HEIGHT/2)

# player2 position
PLAYER2_POSITION = ( SCREEN_WIDTH - (100 + PLAYER_WIDTH) , SCREEN_HEIGHT/2)

#Font
FONT_FAMILY = "arial"
FONT_SIZE = 40
FONT_FAMILY_MENU = "arial"
FONT_SIZE_MENU = 80
FONT_SIZE_SCORE = 45
FONT_SIZE_WIN = 70
FONT_SIZE_PSEUDO = 60

# colors
BLACK = (0,0,0)
WHITE = (255,255,255)
VIOLET = (238,130,238)
RED = (221,36,36)
ORANGE = (229,172,46)

# DatatBase 
DB_NAME = 'myDB.db'
PLAYERSSETTINGSID = 1
PLAYERS_DEFAULT_SETTINGS = [MANEUVERABILITY,
                    ACCELERATION, 
                    BULLET_SPEED, 
                    HEALTH, 
                    DELAY_SHOOT, 
                    POWER_SHOOTING,
                    PLAYERSSETTINGSID]

# Menu
SETTINGS_LIST_NAME = [
            "MANEUVERABILITY",
            "ACCELERATION",
            "BULLET_SPEED",
            "HEALTH",
            "DELAY_SHOOT",
            "POWER_SHOOTING"
        ]