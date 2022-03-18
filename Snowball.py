import pygame
import math

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
#bullet image


class Snowball(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


    def update(self, enemy_group):
        self.rect.y += self.speed

