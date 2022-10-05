import pygame, math, random
from Bullet import *

class Sniper(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 40
        self.radius = 7
        self.damage = 75
        self.reload = 1
        self.xSpeed = math.cos(blob.direction) * self.speed
        self.ySpeed = -math.sin(blob.direction) * self.speed
        self.knockBack = 3
        self.effectSpawn = 10
    
