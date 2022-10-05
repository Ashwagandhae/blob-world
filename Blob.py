import pygame, math, time, random
from Bar import *
from Spammer import *
from Bullet import *
from Sniper import *
from Grenade import *
from RocketLauncher import *
from Effect import *

class Blob(pygame.sprite.Sprite):

    def __init__(self, tempScreen, tempColor, tempEyeColor, tempRadius, tempX, tempY):
        pygame.sprite.Sprite.__init__(self)
        #Measuring the angle from X axisssssss
        self.direction = math.pi / 2
        self.screen = tempScreen
        self.color = tempColor
        self.eyeColor = tempEyeColor
        self.targetRadius = tempRadius
        self.radius = 5
        self.eyeRadius = 15
        self.x = tempX
        self.y = tempY
        self.xSpeed = 0
        self.ySpeed = 0
        self.hungerRate = 0.2
        self.maxHealth = 100        
        self.health = self.maxHealth
        self.healthBar = Bar(self.screen, int(500 - self.maxHealth / 2), 420, (255,255,255), self.maxHealth, "health")
        self.isAlive = True
        self.lastHit = 0
        self.lastEnemy = None
        self.speed = 0.01
        self.brightness = 0
        self.shake = 0
        self.arena = True

    def setDirection(self):
        #get the position
        position = pygame.mouse.get_pos()
        position = list(position)
        #setting the direction
        position[0] = position[0] - self.screen.get_width()/2
        position[1] = - (position[1] - self.screen.get_height()/2)
        self.direction = math.atan2(position[1], position[0])


    def move(self, effectList):
        #do radius
        if self.radius < self.targetRadius:
            self.radius += 5
            if self.radius > self.targetRadius:
                self.radius = self.targetRadius
        elif self.radius > self.targetRadius:
            self.radius -= 5
            if self.radius < self.targetRadius:
                self.radius = self.targetRadius
        #Check if blob in arena or not
        self.arena = not (self.x < 0 or self.x > self.screen.get_width() or self.y < 0 or self.y > self.screen.get_height())
        #get position of the mousey
        position = pygame.mouse.get_pos()
        position = list(position)
        #making X/Y speed
        if self.isAlive:
            self.xSpeed += self.speed * (position[0] - self.screen.get_width()/2)
            self.ySpeed += self.speed * (position[1] - self.screen.get_height()/2)
        else:
            self.xSpeed = 0.02 * (position[0] - self.screen.get_width()/2)
            self.ySpeed = 0.02 * (position[1] - self.screen.get_height()/2)
        #Shaking screen
        if self.shake > 0:
            self.shake -= 2
            self.x += random.randint(int(-self.shake), int(self.shake))
            self.y += random.randint(int(-self.shake), int(self.shake))
            self.brightness += self.shake / 2
        else:
            self.shake = 0
        #setting X/Y speed to int    
        self.xSpeed = int(self.xSpeed * 0.9)
        self.ySpeed = int(self.ySpeed * 0.9)
        #changing X / Y
        self.x += int(self.xSpeed)
        self.y += int(self.ySpeed)

        screenSize = 1000
        if self.x > 1.5 * screenSize:
            self.x = -0.5 * screenSize
        if self.x < -0.5 * screenSize:
            self.x = 1.5 * screenSize
        if self.y > 1.5 * screenSize:
            self.y = -0.5 * screenSize
        if self.y < -0.5 * screenSize:
            self.y = 1.5 * screenSize

        self.x = int(self.x)
        self.y = int(self.y)
        #Spawn effect if outside arena, decrease radius
        if not self.arena and self.isAlive:
            for i in range(random.randint(2, 5)):
                effect = Effect(self.screen, (self.x + random.randint(-self.radius, self.radius), self.y + random.randint(-self.radius, self.radius)), color = self.color)
                effectList.append(effect)
                self.radius -= 1
        
    def draw(self):
        #Do brightness
        if self.brightness > 0:
            self.brightness -= 3
        if self.brightness > 100:
            self.brightness = 100
        if self.brightness < 0:
            self.brightness = 0
        #set the bloboliciouces direction
        self.setDirection()
        #draw blob's body in the middle of screen
        centerX = int(self.screen.get_width()/2)
        centerY = int(self.screen.get_height()/2)
        color = self.color
        Rchange = (255 - color[0]) / 10
        Gchange = (255 - color[1]) / 10
        Bchange = (255 - color[2]) / 10
        drawSize = self.radius
        for i in range(10):
            color = (int(min(255, color[0] + Rchange + self.brightness)), int(min(255, color[1] + Gchange + self.brightness)), int(min(255, color[2] + Bchange + self.brightness)))
            pygame.draw.circle(self.screen, color, (int(self.screen.get_width()/2),int(self.screen.get_height()/2)), drawSize)
            drawSize -= int(self.radius / 10)
        #find eye X and Y
        eyeX = int(centerX + math.cos(self.direction) * 0.65 * self.radius)
        eyeY = int(centerY - math.sin(self.direction) * 0.65 * self.radius)
        #draw an eyeyeyeyeye
        #print(str((int(min(255, self.eyeColor[0] + self.brightness)), int(min(255, self.eyeColor[1] + self.brightness)), int(min(255, self.eyeColor[2] + self.brightness)))))
        pygame.draw.circle(self.screen, (int(min(255, self.eyeColor[0] + self.brightness)), int(min(255, self.eyeColor[1] + self.brightness)), int(min(255, self.eyeColor[2] + self.brightness))), (eyeX, eyeY), self.eyeRadius)
        #draw eye shinyness
        pygame.draw.circle(self.screen, (255, 255, 255), (eyeX + 5, eyeY - 5), int(self.eyeRadius / 3))
        #dawr Health Bar
        self.healthBar.draw(self.health)
            

    def eat(self):
        #If eating food, change health by 20
        self.health += 3

    def tick(self, dev, god):
        #TICKTOKC
        #If hAlth > maxHalth den set halth to maxi hEalthf
        if self.health > self.maxHealth:
            self.health = self.maxHealth
        if self.health <= 0:
            self.isAlive = False
        elif not self.arena:
            #Sloly kill the innocent widdle blobby
            self.health -= 0 if dev or god else self.hungerRate
            #Bury blob
            if self.health <= 0:
                self.isAlive = False
                self.lastEnemy = ["Hunger", "Starvation"]
            
    def takeDamage(self, damage, enemy):
        currentTime = time.time()
        if currentTime - self.lastHit > 0.5:
            #Tke dmage
            self.health -= damage
            #New lathsit time
            self.lastHit = currentTime
            #knockbakc
            self.xSpeed += enemy.xSpeed * 2 * enemy.knockback
            self.ySpeed += enemy.ySpeed * 2 * enemy.knockback
            self.lastEnemy = enemy.nameList
            #Radius
            self.radius -= int(damage * 0.5)
            #Shake
            if self.isAlive:
                self.shake += 20
