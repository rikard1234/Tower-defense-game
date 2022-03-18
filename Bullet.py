import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#bullet image


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle)#convert input angle into radians
        self.speed = 10
        #calculate the horizontal and vertical speeds based on the angle
        self.dx = math.cos(self.angle) * self.speed
        self.dy = -(math.sin(self.angle) * self.speed)


    def update(self):
        #check if bullet has gone off the screen
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()

        #move bullet
        self.rect.x += self.dx
        self.rect.y += self.dy