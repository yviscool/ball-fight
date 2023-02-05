# 324234
# 3234
'''
123123
123123
'''
import pygame
import math
import random

pygame.init()

clock = pygame.time.Clock()

FPS = 60

WIDTH  = 1200
HEIGHT = 800

screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption('球球大战')

pygame.mixer.music.load('backgroundMusic.mp3')
pygame.mixer.music.play(-1)

shoot_fx = pygame.mixer.Sound('shoot.mp3')
enemy_eliminated_fx = pygame.mixer.Sound('enemyEliminated.mp3')

def hsv_to_rgb(h, s, v):
	if s == 0.0: return (v, v, v)
	i = int(h*6.) # XXX assume int() truncates!
	f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
	if i == 0: return (v, t, p)
	if i == 1: return (q, v, p)
	if i == 2: return (p, v, t)
	if i == 3: return (p, q, v)
	if i == 4: return (t, p, v)
	if i == 5: return (v, p, q)


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

		key = pygame.key.get_pressed()
		if key[pygame.K_a] == True:
			self.x -= 5
		if key[pygame.K_d] == True:
			self.x += 5
		if key[pygame.K_w] == True:
			self.y -= 5
		if key[pygame.K_s] == True:
			self.y += 5

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

class Particle:

	def __init__(self, x, y, radius, color, velocity, bg=False):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color
		self.velocity = velocity
		self.counter = 0
		# 阻力
		self.friction = 0.97

		self.is_bg = bg


	def draw(self):
		pygame.draw.circle(
			screen,
			self.color,
			[self.x, self.y],
			self.radius,
		)

	def update(self):
		if not self.is_bg:
			self.velocity[0] *= self.friction
			self.velocity[1] *= self.friction
		self.x += self.velocity[0]
		self.y += self.velocity[1]

		if not self.is_bg:
			self.counter += 1
		else:

			if self.y > WIDTH:
				self.y = 0
				self.x = random.randint(0, WIDTH)



# def create_bg_star():
# 	for i in range(100):
# 		x = random.randint(0, WIDTH)
# 		y = random.randint(0, HEIGHT)
# 		velocity = [
# 			0,
# 			1,
# 		]
# 		radius = random.randint(1, 2)
# 		particle = Particle(x, y, radius, 'white', velocity, True)
# 		particle_list.append(particle)


SPAWN_ENEMY = 500

spawn_enemy_event = pygame.USEREVENT + 1

pygame.time.set_timer(spawn_enemy_event, SPAWN_ENEMY)

run = True

player = Player(WIDTH//2, HEIGHT//2, 30, 'white')

projectile_list = []
enemy_list  = []
particle_list = []

game_over = False

bg = pygame.Surface((WIDTH, HEIGHT))  # the size of your rect
bg.set_alpha(25)                # alpha level
bg.fill((0, 0, 0))           # this fills the entire surface


# create_bg_star()

while run:

	clock.tick(FPS)

	screen.blit(bg, (0,0))
	# screen.fill('white')


	if not game_over:

		player.draw()
		player.update()

		for p in projectile_list:
			p.draw()
			p.update()

			if p.x - p.radius < 0 or p.x + p.radius > WIDTH or\
			   p.y - p.radius < 0 or p.y + p.radius > HEIGHT:
				projectile_list.remove(p)



		for e in enemy_list:
			e.draw()
			e.update()

			# 获取两个点的距离
			dist = pygame.math.Vector2(e.x, e.y).distance_to((player.x, player.y))

			# 如果距离小于 1
			if dist - e.radius - player.radius < 1:
				game_over = True


			for p in projectile_list:

				# 获取两个点的距离
				dist = pygame.math.Vector2(p.x, p.y).distance_to((e.x, e.y))


				# 如果距离小于 1
				if dist - p.radius - e.radius < 1:

					# 粒子特效
					for i in range(e.radius):
						velocity = [
							random.randint(-4, 4),
							random.randint(-4, 4)
						]
						radius = random.randint(1, 3)
						particle = Particle(p.x, p.y, radius, e.color, velocity)
						particle_list.append(particle)

					# 如果敌人大于 20, 那么缩小 10
					if e.radius - 10 > 5:
						e.radius -= 10
						projectile_list.remove(p)
					else:
						enemy_eliminated_fx.play()
						enemy_list.remove(e)
						projectile_list.remove(p)

		for p in particle_list:
			p.draw()
			p.update()
			if p.counter > 50:
				particle_list.remove(p)


	for event in pygame.event.get():

		if event.type == pygame.QUIT:

			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:

			shoot_fx.play()

			pos = pygame.mouse.get_pos()

			# radian = math.atan2(
			# 	pos[1] - HEIGHT // 2,
			# 	pos[0] - WIDTH // 2,
			# )

			radian = math.atan2(
				pos[1] - player.y,
				pos[0] - player.x
			)

			velocity = [
				math.cos(radian) * 8,
				math.sin(radian) * 8,
			]


			# projectile = Projectile(WIDTH//2, HEIGHT//2, 4, 'white', velocity)
			projectile = Projectile(player.x, player.y, 4, 'white', velocity)

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


			# 弧度
			radian = math.atan2(
				HEIGHT // 2 - y,
				WIDTH // 2 - x,
			)

			velocity = [
				math.cos(radian), # 根据弧度获取 x
				math.sin(radian), # 根据弧度获取 y
			]

			# color = [
			# 	random.randint(0, 255),
			# 	random.randint(0, 255),
			# 	random.randint(0, 255),
			# ]

			color = pygame.Color(0)
			color.hsla = (random.randint(0, 360), 50, 50, 100)


			enemy = Enemy(x, y, radius, color, velocity)
			# spawn_enemy_event += 1

			# projectile.draw()
			enemy_list.append(enemy)


	pygame.display.update()

pygame.quit()
