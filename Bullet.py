import pygame, math, random
from Effect import *

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, screen, blob):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = blob.x
        self.y = blob.y
        self.speed = 20
        self.xSpeed = math.cos(blob.direction) * self.speed
        self.ySpeed = -math.sin(blob.direction) * self.speed          
        self.color = blob.color
        self.radius = 10
        self.damage = 30
        self.reload = 0.3
        self.knockBack = 2
        self.canDestroy = 1
        self.bulletAmount = 1
        self.transparency = 100
        self.effectSpawn = 5
        
    def draw(self, blobX, blobY):
        #Draw bullet at correct XY
        if abs(self.xSpeed) > 3 or abs(self.ySpeed) > 3:
            pygame.draw.circle(self.screen, self.color, (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), self.radius + 3)
        pygame.draw.circle(self.screen, (int(255/100 * self.transparency), int(255/100 * self.transparency), int(255/100 * self.transparency)), (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), self.radius)

    def move(self, effectList):
        #Move bullet
        self.x += self.xSpeed
        self.y += self.ySpeed
        self.x = int(self.x)
        self.y = int(self.y)
        #Create effect randomly
        if random.randint(1, self.effectSpawn) == 1:
            effect = Effect(self.screen, (self.x + random.randint(-self.radius, self.radius), self.y + random.randint(-self.radius, self.radius)), color=self.color)
            effectList.append(effect)
        
            
            

