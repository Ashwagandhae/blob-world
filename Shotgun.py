import pygame, math, random
from Bullet import *

class Shotgun(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 40
        self.radius = 7
        self.damage = 75
        self.reload = 1
        self.xSpeed = math.cos(blob.direction) * self.speed + 1
        self.ySpeed = -math.sin(blob.direction) * self.speed + 1
        self.knockBack = 1
        self.bulletAmount = 5
    
