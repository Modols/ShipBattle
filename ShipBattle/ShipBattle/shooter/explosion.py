import datetime, time 
from shooter.utils import load_sprite

class Explosion:
    def __init__(self, position):
        self.position = position
        self.png = "explosion2"
        self.timer = 0.3
        self.createdAt = datetime.datetime.utcfromtimestamp(time.time())
        self.sprite = load_sprite(self.png)

    def checkTimer(self):
        if (datetime.timedelta.total_seconds(datetime.datetime.utcfromtimestamp(time.time()) - self.createdAt) >= self.timer):
            return True
        else:
            return False

    def draw(self, surface):
        surface.blit(self.sprite, self.position)