import pygame, time, random, math
from Bar import *
from Enemy import *

class Whirlpool(Enemy):
    
    def __init__(self, screen, tempX, tempY, tempColor, difficulty):
        super().__init__(screen, tempX, tempY, tempColor, difficulty)
        self.maxHealth = int(200 * self.difficulty)
        self.health = self.maxHealth
        self.healthBar = Bar(self.screen, 0, 0, (255,255,255), self.maxHealth, "health", 125)
        self.eyeRadius = 10
        self.targetRadius = 70
        self.lastWhirl = time.time()
        self.delay = random.randint(5, 15)
        self.whirl = 0
        self.value = 30
        self.points = 15
        self.nameList = ["Whirlpool", "Kraken", "Vortex", "Dragger", "Whirlpool Blob", "Vortex Blob", "Dragging Blob"]

    def draw(self, blobX, blobY):
        #Draw whirl if whirl
        if self.whirl > 0:
            self.whirl -= 15
            color = (int(255 - self.whirl), int(255 - self.whirl), int(255 - self.whirl))
            pygame.draw.circle(self.screen, color, (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), self.whirl)
        else:
            self.whirl = 0

        #Draw enemy
        color = (min(255, self.color[0] + self.brightness), min(255, self.color[1] + self.brightness), min(255, self.color[2] + self.brightness))
        Rchange = int((255 - color[0]) / 10)
        Gchange = int((255 - color[1]) / 10)
        Bchange = int((255 - color[2]) / 10)
        drawSize = self.radius
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.circle(self.screen, color, (int(self.x - blobX + self.screen.get_width() / 2), int(self.y - blobY + self.screen.get_height() / 2)), max(0, drawSize))
            drawSize -= int(self.radius/10)

        #Draw eye
        color = self.color
        color = (int(color[0] / self.eyeDarkness), int(color[1] / self.eyeDarkness), int(color [2] / self.eyeDarkness))
        X = int(self.x - blobX + int(self.screen.get_width() / 2) + self.xSpeed * 3)
        Y = int(self.y - blobY + int(self.screen.get_height() / 2) + self.ySpeed * 3)
        
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
            self.radius += 5
            if self.radius > self.targetRadius:
                self.radius = self.targetRadius
        elif self.radius > self.targetRadius:
            self.radius -= 5
            if self.radius < self.targetRadius:
                self.radius = self.targetRadius
        #Change health size
        self.healthBar.size = int(self.radius * 1.785)
        #Du brytnez
        if self.brightness > 0:
            self.brightness -= 3
        else:
            self.brightness = 0
        #It satlks blawb
        diffX = blobX - self.x
        diffY = blobY - self.y
        distance = math.sqrt(diffX ** 2 + diffY ** 2)
        if self.whirl == 0:
            self.xSpeed = self.xSpeed * 0.7 + 0.3 * (blobX - self.x) / (distance + 1) * 10
            self.ySpeed = self.ySpeed * 0.7 + 0.3 * (blobY - self.y) / (distance + 1) * 10
        else:
            self.xSpeed = 0
            self.ySpeed = 0
            
                        
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
            
    #Chek 4 pull and pool          
    def pull(self, foodList, blob):
        if time.time() - self.lastWhirl > self.delay:
            self.radius -= 20
            self.whirl = 240
            self.lastWhirl = time.time()
            self.delay = random.randint(int(5 / self.difficulty), int(15 / self.difficulty))
            self.xSpeed = 0
            self.ySpeed = 0
            self.brightness += 100
            for food in foodList:
                food.xSpeed += (self.x - food.x) * 0.2 * self.difficulty
                food.ySpeed += (self.y - food.y) * 0.2 * self.difficulty
            blob.xSpeed = (self.x - blob.x) * 0.15 * self.difficulty
            blob.ySpeed = (self.y - blob.y) * 0.15 * self.difficulty
