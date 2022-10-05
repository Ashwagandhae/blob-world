import pygame, math, random
from Bullet import *

class Knife(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 40
        self.radius = 15
        self.damage = 20
        self.reload = 1
        self.xSpeed = math.cos(blob.direction) * self.speed
        self.ySpeed = -math.sin(blob.direction) * self.speed
        self.knockBack = 2
        self.canDestroy = 0
        self.length = 
        
    def move(self):
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.x = int(self.x)
        self.y = int(self.y) 

