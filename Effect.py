import pygame, time, random

class Effect(pygame.sprite.Sprite):
    
    def __init__(self, screen, pos, duration=0.2, targetRadius=5, color=(255,255,255)):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.pos = pos
        self.radius = 5
        self.targetRadius = targetRadius
        self.startTime = time.time()
        self.duration = duration
        self.color = color

    def transformPoint(self, point, blobX, blobY):
        return point[0] - blobX + int(self.screen.get_width() / 2), point[1] - blobY + int(self.screen.get_height() / 2)

    def move(self):
        if self.radius < self.targetRadius:
            self.radius += 1
        elif self.radius > self.targetRadius:
            self.radius -= 1
        if self.startTime + self.duration < time.time():
            self.targetRadius = 0

    def draw(self, blobX, blobY):
        pygame.draw.circle(self.screen, self.color, self.transformPoint(self.pos, blobX, blobY), self.radius)
            
