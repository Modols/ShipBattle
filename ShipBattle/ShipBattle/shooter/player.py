import pygame, datetime, time 
from shooter.utils import load_sprite
from pygame.transform import rotozoom
from pygame.math import Vector2
from shooter.gameObject import GameObject
from shooter.settings import *
from shooter.pirate import Pirate
from shooter.bullet import Bullet

class Player(GameObject):
    def __init__(self, position, joystick_number, pseudo, settings, pngNumber, pngBullet):
        self.pseudo = pseudo
        self.score = 0
        self.direction = Vector2(UP)
        self.position = position
        self.pngName = "ship"
        self.pngNumber = pngNumber
        self.png = f"{self.pngName} ({self.pngNumber})" 
        self.maxHealth = settings[4]

        self.maneuverability = settings[1]
        self.acceleration = settings[2]
        self.bullet_speed = settings[3]
        self.health = settings[4]
        self.delay_shoot = settings[5]
        self.power_shooting = settings[6]

        self.bullets = []
        self.last_time_shoot = datetime.datetime.utcfromtimestamp(time.time())

        self.joystick_number = joystick_number
        self.joystick = pygame.joystick.Joystick(joystick_number)
        self.joystick.init()
        self.pngBullet = pngBullet
        super().__init__(position, load_sprite(self.png), Vector2(0))

    def rotate(self, clockwise):
        if (clockwise != 0):
            sign = clockwise
            angle = self.maneuverability * sign
            self.direction.rotate_ip(angle)

    def accelerate(self):
        self.velocity = self.direction * self.acceleration

    def deceleration(self):
        self.velocity = -self.direction * self.acceleration

    def changeSprite(self, pirates):
        if (self.maxHealth * 1/4) <= self.health and (self.maxHealth * 2/4) >= self.health:
            self.newPngNumber = 12 + self.pngNumber
            self.png = f"{self.pngName} ({self.newPngNumber})"
            self.sprite = load_sprite(self.png)
            pirate = Pirate(self.position)
            pirates.append(pirate)
        elif (self.maxHealth * 2/4) <= self.health and (self.maxHealth * 3/4) >= self.health:
            self.newPngNumber = 6 + self.pngNumber
            self.png = f"{self.pngName} ({self.newPngNumber})"
            self.sprite = load_sprite(self.png)
            pirate = Pirate(self.position)
            pirates.append(pirate)

    def draw(self, surface):
        angle = self.direction.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)

    def updateHealth(self, value):
        self.health = self.health + (value)

    def canShoot(self):
        if(datetime.timedelta.total_seconds(datetime.datetime.utcfromtimestamp(time.time()) - self.last_time_shoot) >= self.delay_shoot):
            self.shoot()
            self.last_time_shoot = datetime.datetime.utcfromtimestamp(time.time())

    def shoot(self):
        bullet_velocity = self.direction * self.bullet_speed  + self.velocity
        bullet = Bullet(self.position, bullet_velocity, self.pngBullet)
        self.bullets.append(bullet)