
import pygame
import math

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


class Projectile:

	def __init__(self, x, y, radius, color, velocity):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.velocity = velocity

	def draw(self):
		pygame.draw.circle(
			screen,
			self.color,
			[self.x, self.y],
			self.radius,
		)

	def update(self):
		self.x += self.velocity[0]
		self.y += self.velocity[1]


run = True

player = Player(WIDTH//2, HEIGHT//2, 30, 'blue')

projectile_list = []


while run:

	clock.tick(FPS)

	screen.fill('white')


	player.draw()
	player.update()

	for p in projectile_list:
		p.draw()
		p.update()

	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:

			pos = pygame.mouse.get_pos()

			radian = math.atan2(
				pos[1] - HEIGHT // 2,
				pos[0] - WIDTH // 2,
			)

			velocity = [
				math.cos(radian),
				math.sin(radian),
			]

			projectile = Projectile(WIDTH//2, HEIGHT//2, 4, 'red', velocity)



			# projectile.draw()
			projectile_list.append(projectile)



	pygame.display.update()

pygame.quit()
