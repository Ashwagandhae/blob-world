import pygame, random

class Food(pygame.sprite.Sprite):
    
    def __init__(self, screen, tempX, tempY, tempColor):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = tempX
        self.y = tempY
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = tempColor
        self.radius = 20
        self.attraction = 0.2

    def draw(self, blobX, blobY):
        #Draw food at correct XY
        Rchange = int((255 - self.color[0]) / 10)
        Gchange = int((255 - self.color[1]) / 10)
        Bchange = int((255 - self.color[2]) / 10)
        color = (0, 0, 0)
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.circle(self.screen, color, (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), self.radius)
            self.radius -= 1
            
        Rchange = int((255 - color[0]) / 10)
        Gchange = int((255 - color[1]) / 10)
        Bchange = int((255 - color[2]) / 10)
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.circle(self.screen, color, (self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2)), self.radius)
            self.radius -= 1

        self.radius = 20

    def goToBlob(self, blobX, blobY):
        self.xSpeed = -int((self.x - blobX) * self.attraction)
        self.ySpeed = -int((self.y - blobY) * self.attraction)
        self.x += self.xSpeed
        self.y += self.ySpeed

    def move(self):
        if abs(self.xSpeed) < 1:
            self.xSpeed += random.randint(-10,10)
        if abs(self.ySpeed) < 1:
            self.ySpeed += random.randint(-10, 10)
        if self.x > self.screen.get_width():
            self.xSpeed += -5
        if self.x < 0:
            self.xSpeed += 5
        if self.y > self.screen.get_height():
            self.ySpeed += -5
        if self.y < 0:
            self.ySpeed += 5
        self.xSpeed *= 0.9
        self.ySpeed *= 0.9
        self.x += int(self.xSpeed)
        self.y += int(self.ySpeed)

