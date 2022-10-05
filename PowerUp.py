import pygame

class PowerUp(pygame.sprite.Sprite):
    
    def __init__(self, screen, tempX, tempY, tempColor, tempType):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = tempX
        self.y = tempY
        self.xSpeed = 0
        self.ySpeed = 0
        self.color = tempColor
        self.size = 60
        self.radius = 40
        self.type = tempType

    def draw(self, blobX, blobY):
        #Draw food at correct XY
        Rchange = int((255 - self.color[0]) / 10)
        Gchange = int((255 - self.color[1]) / 10)
        Bchange = int((255 - self.color[2]) / 10)
        color = (0, 0, 0)
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.rect(self.screen, color, [self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2), self.size, self.size])
            self.size -= 1
            
        Rchange = int((255 - color[0]) / 10)
        Gchange = int((255 - color[1]) / 10)
        Bchange = int((255 - color[2]) / 10)
        for i in range(10):
            color = (color[0] + Rchange, color[1] + Gchange, color[2] + Bchange)
            pygame.draw.rect(self.screen, color, [self.x - blobX + int(self.screen.get_width() / 2), self.y - blobY + int(self.screen.get_height() / 2), self.size, self.size])
            self.size -= 1

        self.size = 60

