import pygame, time, random, math

class Switch(pygame.sprite.Sprite):
    
    def __init__(self, tempScreen, tempRect, tempText=None, tempFont=None, tempSetting=True):
        pygame.sprite.Sprite.__init__(self)
        self.screen = tempScreen
        self.on = tempSetting
        self.rect = pygame.Rect(tempRect)
        self.drawRect = self.rect.copy()
        self.outRect = pygame.Rect(self.rect.x - 5, self.rect.y - 5, self.rect.width + 10, self.rect.width + 10)
        self.circle = 0
        if tempFont is not None:
            self.font = tempFont
            self.text = tempText
        self.distance = self.rect.midright[0] - self.rect.midleft[0]
        if self.rect.centerx > 500:
            self.transitionDistance = 1000 - self.rect.x
        else:
            self.transitionDistance = -self.rect.width - self.rect.x

    def clickedDown(self, mouseDownEvent):
        if self.rect.collidepoint(mouseDownEvent.pos):
            self.mouseButtonDown = True
            return True
        return False
    
    def clickedUp(self, mouseUpEvent):
        ret = None
        if self.rect.collidepoint(mouseUpEvent.pos) and self.mouseButtonDown:
            self.on = not self.on
            ret = self.text
        self.mouseButtonDown = False
        return ret

    def draw(self, color):
        self.circle = int(self.circle)
        
        #outline
        self.outRect = pygame.Rect(self.drawRect.x - 5, self.drawRect.y - 5, self.drawRect.width + 10, self.drawRect.height + 10)
        
        drawColor = (int(100 + 155 / self.distance * self.circle), int(100 + 155 / self.distance * self.circle), int(100 + 155 / self.distance * self.circle))
        pygame.draw.rect(self.screen, drawColor, self.outRect)
        pygame.draw.circle(self.screen, drawColor, self.drawRect.midleft, int(self.outRect.height/2))
        pygame.draw.circle(self.screen, drawColor, self.drawRect.midright, int(self.outRect.height/2))
        
        #inside
        drawColor = (int(color[0] / self.distance * self.circle), int(color[1] / self.distance * self.circle), int(color[2] / self.distance * self.circle))
        pygame.draw.rect(self.screen, drawColor, self.drawRect)
        pygame.draw.circle(self.screen, drawColor, self.drawRect.midleft, int(self.drawRect.height/2))
        pygame.draw.circle(self.screen, drawColor, self.drawRect.midright, int(self.drawRect.height/2))

        #switch
        drawColor = (int(100 + 155 / self.distance * self.circle), int(100 + 155 / self.distance * self.circle), int(100 + 155 / self.distance * self.circle))
        pygame.draw.circle(self.screen, drawColor, (self.drawRect.midleft[0] + self.circle, self.drawRect.centery), int(self.drawRect.height/2 - 3))
        
        if self.on:
            self.circle += self.distance / 5
            if self.circle > self.distance:
                self.circle = self.distance
        else:
            self.circle -= self.distance / 5
            if self.circle < 0:
                self.circle = 0

        #Text
        if self.font is not None:
            drawColor = (int(100 + (color[0] - 100) / self.distance * self.circle), int(100 + (color[1] - 100) / self.distance * self.circle), int(100 + (color[2] - 100) / self.distance * self.circle))
            label = self.font.render(self.text, False, drawColor)
            self.screen.blit(label, (self.drawRect.centerx - self.font.size(self.text)[0] / 2, self.rect.y - int(self.rect.height * 0.5)))

    def transition(self, movement):
        pass
        self.drawRect.x += int(self.transitionDistance * movement)           
