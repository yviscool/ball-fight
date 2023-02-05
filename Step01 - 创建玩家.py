
import pygame

pygame.init()

clock = pygame.time.Clock()

FPS = 60

WIDTH  = 600
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('球球大战')


class Player:


	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color

	def draw(self):

		pygame.draw.circle(
			screen,
			self.color,
			[self.x, self.y],
			self.radius,
		)

	def update(self):
		pass



run = True

player = Player(WIDTH//2, HEIGHT//2, 30, 'blue')

while run:

	clock.tick(FPS)

	screen.fill('white')


	player.draw()
	player.update()

	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			run = False

	pygame.display.update()

pygame.quit()
