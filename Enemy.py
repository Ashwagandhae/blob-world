import pygame, time, random, math
from Bar import *

class Enemy(pygame.sprite.Sprite):
    
    def __init__(self, screen, tempX, tempY, tempColor, difficulty):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.difficulty = difficulty
        self.x = tempX
        self.y = tempY
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = tempColor
        self.targetRadius = 50
        self.radius = 1
        self.eyeRadius = 15
        self.maxHealth = int(100 * self.difficulty)
        self.health = self.maxHealth
        self.healthBar = Bar(self.screen, 0, 0, (255,255,255), self.maxHealth, "health")
        self.eyeDarkness = 2
        self.brightness = 0
        self.value = 20
        self.damage = int(20 * self.difficulty)
        self.knockback = 1 * self.difficulty
        self.points = 10
        self.nameList = ["Frog", "Toad", "Hopper", "Bouncer", "Frog Blob", "Toad Blob", "Hopper Blob", "Bouncer Blob"]
          
    def draw(self, blobX, blobY):
        #Draw enemy
        color = (min(255, self.color[0] + self.brightness), min(255, self.color[1] + self.brightness), min(255, self.color[2] + self.brightness))
        Rchange = int((255 - color[0]) / 10)
        Gchange = int((255 - color[1]) / 10)
        Bchange = int((255 - color[2]) / 10)
        drawSize = self.radius
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.circle(self.screen, color, (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), drawSize)
            drawSize -= int(self.radius / 10)

        #Draw eye
        color = self.color
        color = (int(color[0] / self.eyeDarkness), int(color[1] / self.eyeDarkness), int(color [2] / self.eyeDarkness))
        X = self.x - blobX + int(self.screen.get_width() / 2) + int(self.xSpeed) * 2
        Y = self.y - blobY + int(self.screen.get_height() / 2) + int(self.ySpeed) * 2
        
        pygame.draw.circle(self.screen, color, (X,Y), self.eyeRadius)
        
        #Draw eeye shyniness
        pygame.draw.circle(self.screen, (255,255,255), (X + 5,Y - 5), int(self.eyeRadius / 3))

        #Draw eyebrow
        pygame.draw.rect(self.screen, self.color, (X - self.eyeRadius, Y - self.eyeRadius, 30, 10))
                           
        #Draw healthBar
        self.healthBar.x = self.x - blobX + int(self.screen.get_width() / 2) - int(self.healthBar.size / 2)
        self.healthBar.y = self.y - blobY + int(self.screen.get_height() / 2) - (self.radius + 30)
        self.healthBar.draw(self.health)
        
    def move(self, blobX, blobY):
        #do radius
        if self.radius < self.targetRadius:
            self.radius += 5
            if self.radius > self.targetRadius:
                self.radius = self.targetRadius
        elif self.radius > self.targetRadius:
            self.radius -= 5
            if self.radius < self.targetRadius:
                self.radius = self.targetRadius
        #Change health size
        self.healthBar.size = int(self.radius * 2)
        #do brightness
        if self.brightness > 0:
            self.brightness -= 3
        else:
            self.brightness = 0

        #BounceModes
        if abs(self.xSpeed) > 1 or abs(self.ySpeed) > 1:
            self.xSpeed *= 0.9
            self.ySpeed *= 0.9
        else:
            #Random
            """self.xSpeed = random.randint(-20, 20)
            self.ySpeed = random.randint(-20, 20)"""
            #Chase
            """diffX = blobX - self.x
            diffY = blobY - self.y
            distance = math.sqrt(diffX ** 2 + diffY ** 2)
            self.xSpeed = int((blobX - self.x) / distance * 20)
            self.ySpeed = int((blobY - self.y) / distance * 20)"""
            #Combo
            if random.randint(1, 2) == 1:
                diffX = blobX - self.x
                diffY = blobY - self.y
                distance = math.sqrt(diffX ** 2 + diffY ** 2)
                self.xSpeed = (blobX - self.x) / distance * 20 
                self.ySpeed = (blobY - self.y) / distance * 20
            else:
                self.xSpeed = random.randint(-20, 20)
                self.ySpeed = random.randint(-20, 20)
        #Change XY
        self.x += int(self.xSpeed * self.difficulty)
        self.y += int(self.ySpeed * self.difficulty)
        #Bounce of borders
        if self.x > self.screen.get_width():
            self.xSpeed += -5
        if self.x < 0:
            self.xSpeed += 5
        if self.y > self.screen.get_height():
            self.ySpeed += -5
        if self.y < 0:
            self.ySpeed += 5


    def takeDamage(self, damage, bullet):
        if bullet.xSpeed > 0 or bullet.ySpeed > 0:
            self.xSpeed = int((self.xSpeed + bullet.xSpeed * bullet.knockBack) * 0.5)
            self.ySpeed = int((self.ySpeed + bullet.xSpeed * bullet.knockBack) * 0.5)
        else:
            self.xSpeed += 0.05 * (50 - (bullet.x - self.x))
            self.ySpeed += 0.05 * (50 - (bullet.y - self.y))
        self.health -= damage
        self.radius -= int(damage * 0.5)
        self.radius = max(self.radius, 1)
        self.brightness += int(damage * 2)
