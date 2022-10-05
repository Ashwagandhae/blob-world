import pygame, math, time, random

class Button(pygame.sprite.Sprite):

    def __init__(self, screen, XY, tempText, tempFont):
        pygame.sprite.Sprite.__init__(self)
        self.screen = screen
        self.text = tempText
        self.font = tempFont
        self.rect = pygame.Rect(XY, (self.font.size(self.text)[0] + 20, self.font.size(self.text)[1] + 15))
        self.drawRect = self.rect.copy()
        self.pressedRect = pygame.Rect((self.rect[0] + 5, self.rect[1] + 5, self.rect[2] - 10, self.rect[3] - 10))
        self.mouseButtonDown = False
        self.label = self.font.render(self.text, False, (255,255,255))
        self.offset = 0
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
        if self.rect.collidepoint(mouseUpEvent.pos) and self.mouseButtonDown:
            ret = self.text
        self.mouseButtonDown = False
        return ret

    def colorShade(self, color, change):
        return (min(255, max(0, color[0] + change)), min(255, max(0, color[1] + change)), min(255, max(0, color[2] + change)))
    
    def draw(self, color):
        if self.mouseButtonDown:
            self.roundedRect(self.screen, self.pressedRect, self.colorShade(color, -20), 0.4)
            self.screen.blit(self.label, (self.pressedRect.x + 5, self.pressedRect.y + 5))
        else:
            self.roundedRect(self.screen, self.drawRect, color, 0.4)
            self.screen.blit(self.label, (self.drawRect.x + 10, self.drawRect.y + 10))

    def transition(self, movement):
        self.drawRect.x += int(self.transitionDistance * movement)
            
