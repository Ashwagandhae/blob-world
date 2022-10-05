import pygame, math, random
from Bullet import *

class Grenade(Bullet):
    
    def __init__(self, screen, blob): 
        super().__init__(screen, blob)
        self.speed = 60
        self.radius = 15
        self.damage = 3
        self.reload = 1
        self.xSpeed = math.cos(blob.direction) * self.speed
        self.ySpeed = -math.sin(blob.direction) * self.speed
        self.knockBack = 0
        self.canDestroy = 0
        self.effectSpawn = 10
        
    def move(self, effectList):
        if abs(self.xSpeed) > 3 or abs(self.ySpeed) > 3:
            self.xSpeed *= 0.9
            self.ySpeed *= 0.9
            self.x += self.xSpeed
            self.y += self.ySpeed
            self.x = int(self.x)
            self.y = int(self.y)
            #Create effect randomly
            if random.randint(1, self.effectSpawn) == 1:
                effect = Effect(self.screen, (self.x + random.randint(-self.radius, self.radius), self.y + random.randint(-self.radius, self.radius)), color=self.color)
                effectList.append(effect)
        else:
            self.radius += 10
            
