from shooter.gameObject import GameObject
from shooter.utils import load_sprite

class Bullet(GameObject):
    def __init__(self, position, velocity, pngBullet):
        super().__init__(position, load_sprite(pngBullet), velocity)

    def move(self):
        self.position = self.position + self.velocity
