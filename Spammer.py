import pygame, math, random
from Bullet import *

class Spammer(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 30
        self.radius = 7
        self.damage = 8
        self.reload = 0.1
        self.xSpeed = math.cos(blob.direction) * self.speed * random.randint(7, 13) / 10
        self.ySpeed = -math.sin(blob.direction) * self.speed * random.randint(7, 13) / 10
        self.knockBack = 1.5
