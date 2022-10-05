import pygame, time, random, math

class Message(pygame.sprite.Sprite):
    
    def __init__(self, tempScreen, tempFont, tempText, tempType, tempTime=0):
        pygame.sprite.Sprite.__init__(self)
        self.screen = tempScreen
        self.text = tempText
        self.font = tempFont
        self.type = tempType
        self.textRect = pygame.Rect(self.screen.get_width() / 2 - self.font.size(self.text)[0] / 2, -self.font.size(self.text)[1] - 20, self.font.size(self.text)[0], self.font.size(self.text)[1])
        self.rect = pygame.Rect(self.textRect.x - 10, self.textRect.y - 10, self.textRect.width + 20, self.textRect.height + 20)
        self.outRect = pygame.Rect(self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, self.rect.height + 8)
        self.startTime = None
        self.showTime = tempTime

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

    def drawMove(self, color, speed):
        if self.startTime == None:
            self.startTime = time.time()
        if self.showTime > 0:
            if time.time() < self.startTime + (self.showTime / speed):
                #moving rect
                if self.rect.y < 30:
                    self.rect.y += 10 * speed if 10 * speed < 55 else 55
                    if self.rect.y > 30:
                        self.rect.y = 30
            else:
                #moving rect
                if self.rect.y > -self.font.size(self.text)[1] - 30:
                    self.rect.y += -10 * speed if -10 * speed > -55 else -55
                else:
                    self.showTime = None
                
            #resetting rects
            self.textRect = pygame.Rect(self.rect.x + 10, self.rect.y + 10, self.rect.width - 20, self.rect.width - 20)
            self.outRect = pygame.Rect(self.rect.x - 4, self.rect.y - 4, self.rect.width + 8, self.rect.height + 8)

            #Outline
            if self.type == "info":
                self.roundedRect(self.screen, self.outRect, color, 0.4)
            else:
                self.roundedRect(self.screen, self.outRect, (255,0,0), 0.4)

            #Inside
            self.roundedRect(self.screen, self.rect, (0,0,0), 0.4)

            #Text
            if self.type == "info" or self.type == "error":
                label = self.font.render(self.text, False, (255,255,255))
                self.screen.blit(label, (self.textRect.x, self.textRect.y))
            elif self.type == "greeting":
                greetingLabel = self.font.render(self.text[0], False, (255,255,255))
                nameLabel = self.font.render(self.text[1], False, color)
                self.screen.blit(greetingLabel, (self.textRect.x, self.textRect.y))
                self.screen.blit(nameLabel, (self.textRect.x + self.font.size(self.text[0])[0], self.textRect.y))


