import pygame, math, random
from Bullet import *

class EnemyBullet(Bullet):
    
    def __init__(self, screen, enemy, nameList, difficulty):
        super().__init__(screen, enemy)
        self.xSpeed = enemy.xSpeed * 3 * difficulty
        self.ySpeed = enemy.ySpeed * 3 * difficulty
        self.color = enemy.color
        self.knockback = int(1.5 * difficulty)
        self.damage = int(30 * difficulty)
        self.nameList = nameList
