import pygame
import math
from Bullet import Bullet
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
class Castle():
    def __init__(self, image100, image50, image25,  x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False
        self.money = 5000
        self.score = 0

        width = image100.get_width()
        height = image100.get_height()

        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))

        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y


    def shoot(self, bullet_img, bullet_group):
        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.midleft[0]
        y_dist = -(pos[1] - self.rect.midleft[1])
        self.angle = math.degrees(math.atan2(y_dist, x_dist))
        #get mouseclick
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 200:
            self.fired = True
            bullet = Bullet(bullet_img, self.rect.midleft[0], self.rect.midleft[1], self.angle)
            bullet_group.add(bullet)
        #reset mouseclick
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False



    def draw(self):
        #check which img to use based on health
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        screen.blit(self.image, self.rect)

    def repair(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.health += 500
            self.money -= 1000
            if self.health > self.max_health:
                self.health = self.max_health
    def armour(self):
        if self.money >= 1000 and self.health < self.max_health:
            self.max_health += 500
            self.money -= 1000