import pygame, time, random, math
from Bar import *
from Enemy import *

class FastEnemy(Enemy):
    
    def __init__(self, screen, tempX, tempY, tempColor, difficulty):
        super().__init__(screen, tempX, tempY, tempColor, difficulty)
        self.maxHealth = 20 * self.difficulty
        self.health = self.maxHealth
        self.healthBar = Bar(self.screen, 0, 0, (255,255,255), self.maxHealth, "health", 70)
        self.eyeRadius = 10
        self.targetRadius = 15
        self.value = 3
        self.damage = int(8 * self.difficulty)
        self.knockback = int(0.1 * self.difficulty)
        self.points = 2
        self.nameList = []

#Draw
    def draw(self, blobX, blobY):
        #Draw enemy
        color = (min(255, self.color[0] + self.brightness), min(255, self.color[1] + self.brightness), min(255, self.color[2] + self.brightness))
        Rchange = int((255 - color[0]) / 10)
        Gchange = int((255 - color[1]) / 10)
        Bchange = int((255 - color[2]) / 10)
        drawSize = self.radius
        for i in range(5):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.circle(self.screen, color, (int(self.x - blobX + self.screen.get_width() / 2), int(self.y - blobY + self.screen.get_height() / 2)), drawSize)
            drawSize -= int(self.radius/5)

        #Draw eye
        color = self.color
        color = (int(color[0] / self.eyeDarkness), int(color[1] / self.eyeDarkness), int(color [2] / self.eyeDarkness))
        X = self.x - blobX + int(self.screen.get_width() / 2)
        Y = self.y - blobY + int(self.screen.get_height() / 2)
        
        pygame.draw.circle(self.screen, color, (X,Y), self.eyeRadius)
        
        #Draw eeye shyniness
        pygame.draw.circle(self.screen, (255,255,255), (X + 5,Y - 5), int(self.eyeRadius / 3))

        #Draw eyebrow
        pygame.draw.rect(self.screen, self.color, (X - self.eyeRadius, Y - self.eyeRadius, 15, 5))
                           
        #Draw healthBar
        self.healthBar.x = self.x - blobX + int(self.screen.get_width() / 2) - int(self.healthBar.size / 2)
        self.healthBar.y = self.y - blobY + int(self.screen.get_height() / 2) - (self.radius + 30)
        self.healthBar.draw(self.health)
        
#Moove                
    def move(self, blobX, blobY):
        #do radius
        if self.radius < self.targetRadius:
            self.radius += 1
            if self.radius > self.targetRadius:
                self.radius = self.targetRadius
        elif self.radius > self.targetRadius:
            self.radius -= 1
            if self.radius < self.targetRadius:
                self.radius = self.targetRadius
        #Change health size
        self.healthBar.size = int(self.radius * 4.666)
        #Du brytnez
        if self.brightness > 0:
            self.brightness -= 3
        else:
            self.brightness = 0
        #It satlks blawb
        diffX = blobX - self.x
        diffY = blobY - self.y
        distance = math.sqrt(diffX ** 2 + diffY ** 2)
        self.xSpeed += (blobX - self.x) / (distance + 1) * 10
        self.ySpeed += (blobY - self.y) / (distance + 1) * 10
        #Bounce of borders
        if self.x > self.screen.get_width():
            self.xSpeed = -20
        if self.x < 0:
            self.xSpeed = 20
        if self.y > self.screen.get_height():
            self.ySpeed = -20
        if self.y < 0:
            self.ySpeed = 20
        #Change XY
        self.x += int(self.xSpeed * self.difficulty)
        self.y += int(self.ySpeed * self.difficulty)
