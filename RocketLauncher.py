import pygame, math, random
from Bullet import *

class RocketLauncher(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 40
        self.radius = 15
        self.damage = 4
        self.reload = 1.5
        self.xSpeed = math.cos(blob.direction) * self.speed
        self.ySpeed = -math.sin(blob.direction) * self.speed
        self.knockBack = 0
        self.canDestroy = 0
        self.effectSpawn = 1
        
    def move(self, effectList):
        if abs(self.xSpeed) > 2 and abs(self.ySpeed) > 2:
            self.x += self.xSpeed
            self.y += self.ySpeed
            self.x = int(self.x)
            self.y = int(self.y)
            #Create effect randomly
            if random.randint(1, self.effectSpawn) == 1:
                effect = Effect(self.screen, (self.x + random.randint(-self.radius, self.radius), self.y + random.randint(-self.radius, self.radius)), color=self.color, targetRadius=20)
                effectList.append(effect)
        else:
            self.radius += 10
