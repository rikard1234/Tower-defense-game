import pygame
class Friend(pygame.sprite.Sprite):
    def __init__(self, health, animation_list, x, y, speed):
        pygame.sprite.Sprite.__init__(self)
        self.fighting_with_boss = False
        self.list = []
        self.got_target = False
        self.alive = True
        self.speed = speed
        self.health = health
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = 0 #0 walk 1: attack 2:death
        self.update_time = pygame.time.get_ticks()
        self.last_attack = pygame.time.get_ticks()
        self.attack_cooldown = 1000
        #select starting image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0,0,25,40)
        self.rect.center = (x, y)

    def update(self, surface, target, enemy_group, boss_group):
        if self.alive:
            #check for collision with bullets
            #if pygame.sprite.spritecollide(self, enemy_group, True) and self.got_target:

            if pygame.sprite.spritecollide(self, enemy_group, False):
                self.list = pygame.sprite.spritecollide(self, enemy_group, False)
                self.update_action(1)
            elif pygame.sprite.spritecollide(self, boss_group, False):
                self.list = pygame.sprite.spritecollide(self, boss_group, False)
                self.fighting_with_boss = True
                self.update_action(1)
            else:
                self.update_action(0)
                self.fighting_with_boss = False

            #move enemy
            if self.action == 0:
                self.rect.x -= self.speed

            if self.action == 1:
                #check if enough time passed since last attacked
                if pygame.time.get_ticks() - self.last_attack > self.attack_cooldown:
                    print(len(self.list))
                    print(self.health)
                    if(self.fighting_with_boss):
                        self.health -= 100
                        self.fighting_with_boss = False
                    else:
                        self.health = self.health - 5 - 3 * len(self.list)
                    self.last_attack = pygame.time.get_ticks()

            if self.health <= 0:
                self.kill()

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







