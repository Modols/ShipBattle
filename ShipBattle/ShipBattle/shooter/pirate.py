from random import randrange
from shooter.utils import load_sprite

class Pirate:
    def __init__(self, position):
        self.position = position
        self.randNumber = randrange(4) + 1
        self.png = f"crew ({self.randNumber})"
        self.sprite = load_sprite(self.png)

    def draw(self, surface):
        surface.blit(self.sprite, self.position)
