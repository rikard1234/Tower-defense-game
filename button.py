import pygame

#button class
class Button():
	def __init__(self, x, y, image, scale, image1 = None):
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.image1 = image1
		if self.image1 is not None:
			self.image1 = pygame.transform.scale(image1, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def draw(self, surface):
		action = False
		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if self.rect.collidepoint(pos) and self.image1 is not None:
			surface.blit(self.image1, (self.rect.x, self.rect.y))

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action
