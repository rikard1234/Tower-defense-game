import pygame
from Friend import Friend
class Boss(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.reacting_to_wind = False
        self.list = []
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 #0 walk 1: attack 2:death
        self.update_time = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.last_hit = pygame.time.get_ticks()
        self.reacting_time = 500
        self.attack_cooldown = 1000
        #select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,100,400)
        self.rect.center = (x, y)

    def react_to_wind(self):
        print("cipka")
        self.reacting_to_wind = True

    def update(self, surface, target, bullet_group, friend_group, snowball_group):
        if self.alive:
            #if pygame.sprite.spritecollide(self, snowball_group, True):
                #self.health = 0
            if self.reacting_to_wind == True:
                if self.reacting_time - pygame.time.get_ticks() > -5000:
                    print(self.reacting_time - pygame.time.get_ticks())
                    self.rect.x -= 1
                else:
                    print("jwaj")
                    self.reacting_time = pygame.time.get_ticks()
                    self.reacting_to_wind = False

            #check for collision with bullets
            if pygame.sprite.spritecollide(self, friend_group, False):
                self.list = pygame.sprite.spritecollide(self, friend_group, False)
                self.update_action(1)
            if not pygame.sprite.spritecollide(self, friend_group, False) and not self.rect.right > target.rect.left and not self.health <= 0:
                self.update_action(0)
            if pygame.sprite.spritecollide(self, bullet_group, True):
                print('hit')
                #lower enemy health
                self.health -= 25
            #check if enemy has reached the castle
            if self.rect.right > target.rect.left:
                self.update_action(1)

            #move enemy
            if self.action == 0 and self.reacting_to_wind == False:
                self.rect.x += self.speed

            if self.action == 1:
                #check if enough time passed since last attacked
                if pygame.time.get_ticks() - self.last_hit > self.attack_cooldown and pygame.sprite.spritecollide(self, friend_group, False):
                    self.health = self.health - 2 * len(self.list)
                    self.last_attack = pygame.time.get_ticks()

                elif pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    target.health -= 100
                    if target.health < 0:
                        target.health = 0
                    self.last_attack = pygame.time.get_ticks()


            if self.health <= 0:
                target.money += 5000
                target.score += 100
                self.update_action(2)
                self.alive = False
                print(self.action)

        self.update_animation()
        #draw image om screen
        surface.blit(self.image, (self.rect.x - 10, self.rect.y-15))

    def update_animation(self):
        #define animation cooldown
        ANIMATION_COOLDOWN = 50
        #update image depending on currenct action
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            #animation resetting
            if self.frame_index >= len(self.animation_list[self.action]):
                if self.action == 2:
                    self.frame_index = len(self.animation_list[self.action]) - 1
                else:
                    self.frame_index = 0

    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
        #update the animatio  settings
            self.frame_index = 0
            self.update_date = pygame.time.get_ticks()







