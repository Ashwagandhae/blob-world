import pygame, math, time, random

class TextBox(pygame.sprite.Sprite):

    def __init__(self, tempScreen, tempRect, tempFont, tempNoText):
        pygame.sprite.Sprite.__init__(self)
        self.screen = tempScreen
        self.text = ""
        self.noText = tempNoText
        self.font = tempFont
        self.rect = pygame.Rect(tempRect)
        self.textRect = pygame.Rect((self.rect[0] + 15, self.rect[1] + 5), self.font.size(self.text))
        self.drawRect = self.rect.copy()
        self.innerRect = pygame.Rect((self.drawRect[0] + 4, self.rect[1] + 4, self.rect[2] - 8, self.rect[3] - 8))
        self.noTextLabel = self.font.render(self.noText, False, (100,100,100))
        self.mouseButtonDown = False
        self.focus = False
        self.blinker = None
        self.blinkerCount = 0
        self.offset = 0
        self.hide = False
        self.hideAnimation = [int(-self.font.size(self.text)[1] * 0.1), 2]
        if self.rect.centerx > 500:
            self.transitionDistance = 1000 - self.rect.x
        else:
            self.transitionDistance = -self.rect.width - self.rect.x

    def roundedRect(self, surface, rect, color, radius=0.7):
        rect = pygame.Rect(rect)
        color = pygame.Color(*color)
        alpha = color.a
        color.a = 0
        pos = rect.topleft
        rect.topleft = 0,0
        rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

        circle = pygame.Surface([min(rect.size)*3]*2, pygame.SRCALPHA)
        pygame.draw.ellipse(circle,(0,0,0),circle.get_rect(),0)
        circle = pygame.transform.smoothscale(circle,[int(min(rect.size)*radius)]*2)

        radius = rectangle.blit(circle,(0,0))
        radius.bottomright = rect.bottomright
        rectangle.blit(circle,radius)
        radius.topright = rect.topright
        rectangle.blit(circle,radius)
        radius.bottomleft = rect.bottomleft
        rectangle.blit(circle,radius)

        rectangle.fill((0,0,0),rect.inflate(-radius.w,0))
        rectangle.fill((0,0,0),rect.inflate(0,-radius.h))

        rectangle.fill(color,special_flags = pygame.BLEND_RGBA_MAX)
        rectangle.fill((255,255,255,alpha),special_flags = pygame.BLEND_RGBA_MIN)

        return surface.blit(rectangle,pos)

    def clickedDown(self, mouseDownEvent):
        if self.rect.collidepoint(mouseDownEvent.pos):
            self.mouseButtonDown = True
            return True
        return False

    def clickedUp(self, mouseUpEvent):
        ret = None
        self.focus = False
        if self.rect.collidepoint(mouseUpEvent.pos) and self.mouseButtonDown:
            ret = self.noText
            self.focus = True
        else:
            self.focus = False
        self.mouseButtonDown = False
        return ret

    def colorShade(self, color, change):
        return (min(255, max(0, color[0] + change)), min(255, max(0, color[1] + change)), min(255, max(0, color[2] + change)))

    def hiddenText(self, color):
        self.hideAnimation[0] += self.hideAnimation[1]
        if abs(self.hideAnimation[0]) > 10:
            self.hideAnimation[0] -= self.hideAnimation[1]
            self.hideAnimation[1] = -self.hideAnimation[1]
        size = self.hideAnimation[0]
        sizeChange = self.hideAnimation[1]
        for i in range(len(self.text)):
            size += sizeChange
            if abs(size) > 10:
                size -= sizeChange
                sizeChange = -sizeChange
            pygame.draw.circle(self.screen, color, (int(self.textRect.x + self.textRect.width / len(self.text) * i), self.rect.centery), int(self.font.size(self.text)[1] * 0.2 + size))
                               
    def draw(self, color):
        if self.text == "":
            label = self.noTextLabel
        else:
            label = self.font.render(self.text, False, (255,255,255))

        if self.font.size(self.text)[0] + 25 < self.rect.width:
            self.textRect = pygame.Rect((self.rect.x + 15, self.rect.y + self.textRect.height/4), self.font.size(self.text))
        else:
            self.textRect = pygame.Rect((self.rect.midright[0] - self.textRect.width - 25, self.rect.y + self.textRect.height/4), self.font.size(self.text))
        
        if self.focus:
            #Draw Box
            self.roundedRect(self.screen, self.drawRect, color, radius=0.4)
            self.roundedRect(self.screen, self.innerRect, (0,0,0), radius=0.4)

            #Draw Text or hidden text
            if self.hide and self.text != "":
                self.hiddenText((255,255,255))
            else:
                self.screen.blit(label, (self.textRect.x, self.textRect.y))
            
            #Blinker
            self.blinkerCount += 1

            self.blinkerCount %= 20

            #Blinker Shade
            shade = int(abs(-10 + self.blinkerCount) * 255/10)
            
            #Draw Blinker
            if self.font.size(self.text)[0] + 25 < self.rect.width:
                xy = (self.textRect.x + self.textRect.width + -7 if self.text == "" else self.textRect.x + self.textRect.width + 3, self.rect.y + 8)
            else:
                xy = (self.rect.midright[0] - 25, self.rect.y + 8)
            self.blinker = pygame.Rect(xy, (8, 82))
            pygame.draw.rect(self.screen, (shade,shade,shade), self.blinker)
            
        else:
            #Draw Box
            self.roundedRect(self.screen, self.drawRect, (100,100,100), radius=0.4)
            self.roundedRect(self.screen, self.innerRect, (0,0,0), radius=0.4)
            
            #Draw Text or hidden text
            if self.hide and self.text != "":
                self.hiddenText((255,255,255))
            else:
                self.screen.blit(label, (self.textRect.x, self.textRect.y))
            
        #Draw Overtext Blocker
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(0, self.rect.y, self.rect.midleft[0], self.rect.height))
        pygame.draw.rect(self.screen, (0,0,0), pygame.Rect(self.rect.midright[0], self.rect.y, self.screen.get_width() - self.rect.midright[0], self.rect.height))


    def transition(self, movement):
        self.drawRect.x += int(self.transitionDistance * movement)
        self.innerRect.x += int(self.transitionDistance * movement)
