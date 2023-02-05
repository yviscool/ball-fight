
import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()

FPS = 60

WIDTH  = 800
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


class Enemy:

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


SPAWN_ENEMY = 500

spawn_enemy_event = pygame.USEREVENT + 1

pygame.time.set_timer(spawn_enemy_event, SPAWN_ENEMY)

run = True

player = Player(WIDTH//2, HEIGHT//2, 30, 'blue')

projectile_list = []
enemy_list  = []


while run:

	clock.tick(FPS)

	screen.fill('white')


	player.draw()
	player.update()

	for p in projectile_list:
		p.draw()
		p.update()

	for e in enemy_list:
		e.draw()
		e.update()

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

		if event.type == spawn_enemy_event:

			pos = pygame.mouse.get_pos()

			radius = random.randint(5, 30)

			# 第一种
			# x = random.randint(0, WIDTH)
			# x = 0 - radius
			# y = random.randint(0, HEIGHT)

			# 第二种
			# if random.randint(0, 10) < 5:
			# 	x = 0 - radius
			# else:
			# 	x = WIDTH - radius

			# if random.randint(0, 10) < 5:
			# 	y = 0 - radius
			# else:
			# 	y = HEIGHT - radius

			# 第三种
			if random.randint(0, 10) < 5:
				if random.randint(0, 10) < 5:
					x = 0 - radius
				else:
					x = WIDTH - radius
				y = random.randint(0, HEIGHT)
			else:
				if random.randint(0, 10) < 5:
					y = 0 - radius
				else:
					y = HEIGHT - radius

				x = random.randint(0, WIDTH)


			radian = math.atan2(
				HEIGHT // 2 - y,
				WIDTH // 2 - x,
			)

			velocity = [
				math.cos(radian),
				math.sin(radian),
			]


			enemy = Enemy(x, y, radius, 'green', velocity)

			# projectile.draw()
			enemy_list.append(enemy)


	pygame.display.update()

pygame.quit()
