import pygame

class Bar(pygame.sprite.Sprite):
    
    def __init__(self, screen, tempX, tempY, tempColor, varMax, tempLabel, tempSize=100, tempHeight=20):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.x = tempX
        self.y = tempY
        self.color = tempColor
        self.var = 0
        self.varMax = varMax
        self.size = tempSize
        self.height = tempHeight
        
    def draw(self, var, color=None):
        #Check if color passed in
        if color is not None:
            self.color = color
        self.var = var
        #Draw outline
        pygame.draw.rect(self.screen, (100, 100, 100), [self.x - 5, self.y - 5, int(self.size) + 10, self.height + 10])
        pygame.draw.circle(self.screen, (100, 100, 100), (self.x, self.y + int(self.height / 2)), int((self.height + 10) / 2))
        pygame.draw.circle(self.screen, (100, 100, 100), (self.x + self.size, self.y + int(self.height / 2)), int((self.height + 10) / 2))
        #Draw bar
        pygame.draw.rect(self.screen, self.color, [self.x, self.y, int(self.var / self.varMax * self.size), self.height])
        pygame.draw.circle(self.screen, self.color, (self.x, self.y + int(self.height / 2)), int(self.height / 2))
        pygame.draw.circle(self.screen, self.color, (self.x + int(self.var / self.varMax * self.size), self.y + int((self.height / 2))), int(self.height / 2))
