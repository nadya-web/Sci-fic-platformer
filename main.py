import pygame
from os import path
import random
import csv


pygame.init()
window = pygame.display.set_mode((1000, 1000))
running = True

pl_walk_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pl_walk_sprites')
standing_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pl_standing_sprites')
pl_death_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pl_death')
enemy_walk_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'enemy_walk')
enemy_death_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'enemy_death')
pics_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pics')
bg_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'bg')

ground = pygame.image.load(path.join(bg_dir, 'ground.png'))
ground = pygame.transform.scale(ground, (2300, 1000))
sky = pygame.image.load(path.join(bg_dir, 'sky.png'))
sky = pygame.transform.scale(sky, (2300, 1000))
mountaines1 = pygame.image.load(path.join(bg_dir, 'mountaines1.png'))
mountaines1 = pygame.transform.scale(mountaines1, (2300, 1000))
mountaines2 = pygame.image.load(path.join(bg_dir, 'mountaines2.png'))
mountaines2 = pygame.transform.scale(mountaines2, (2300, 1000))
pl_walk_right = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_walk_left = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'l{i}.png')), range(1, 12)))
pl_standing_right = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_standing_left = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'l{i}.png')), range(1, 12)))
pl_death = list(map(lambda i: pygame.image.load(path.join(pl_death_dir, f'{i}.png')), range(1, 27)))
enemy_death = list(map(lambda i: pygame.image.load(path.join(enemy_death_dir, f'{i}.png')), range(2, 21)))
health_bars = list(map(lambda i: pygame.image.load(path.join(pics_dir, f'{i}.png')), range(1,7)))
blocks = list(map(lambda i: pygame.image.load(path.join(pics_dir, f'block{i}.png')), range(1,13)))
avatar = pygame.image.load(path.join(pics_dir, 'avatar.png'))
btn = pygame.image.load(path.join(pics_dir, 'start_btn.png'))
logo = pygame.image.load(path.join(pics_dir, 'logo.png'))
enemy = pygame.image.load(path.join(pics_dir, 'r1.png'))
fuel = pygame.image.load(path.join(pics_dir, 'fuel.png'))
pl = pygame.image.load(path.join(pics_dir, 'pl.png'))


btn = pygame.transform.scale(btn, (232, 96))
logo = pygame.transform.scale(logo, (595, 230))

ROWS = 16
MAX_COLS = 150
TILE_SIZE = 64
level = 2

SCROLL_FRAME = 200
scroll = 0
bg_scroll = 0

TILES = blocks
TILES.append(enemy)
TILES.append(fuel)
TILES.append(pl)

class World():
    def __init__(self):
        self.list = list()

    def process_data(self, data):
        global enemies
        player = 0
        for y, row in enumerate(data):
            for x, tile in enumerate(row):
                if tile > -1:
                    img = TILES[tile]
                    coords = [x * 64, y * 64]
                    if tile >= 0 and tile < 12:
                        self.list.append([img, coords])
                    elif tile == 12:
                        enemy = Enemy(x * TILE_SIZE - 50, y * TILE_SIZE - 43, x * TILE_SIZE + 100)
                        enemies.append(enemy)
                    elif tile == 13:
                        fuel = Fuel(img, x * TILE_SIZE, y * TILE_SIZE)
                        fuels.append(fuel)
                    elif tile == 14 and player == 0:
                        player = Player(x * TILE_SIZE - 192, y * TILE_SIZE - 114)
        return player

    def draw(self):
        global scroll
        for tile in self.list:
            tile[1][0] += scroll
            window.blit(tile[0], tile[1])


class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 256
        self.hight = 256
        self.velocity = 10
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.steps = 0
        self.standing = 0
        self.side = 1
        self.hitbox = (self.x + 105, self.y + 75, 40, 105)
        self.life = 0
        self.death = 0
        self.death_loop = 0

    def draw(self, window):
        global start_game
        if self.life < 5:
            if self.steps + 1 >= 30:
                self.steps = 0
            if self.right:
                player = pl_walk_right[self.steps // 3]
                player.set_colorkey((255, 255, 255))
                window.blit(player, (self.x, self.y))
                self.steps += 1
                self.standing = self.steps
            elif self.left:
                player = pl_walk_left[self.steps // 3]
                player.set_colorkey((255, 255, 255))
                window.blit(player, (self.x, self.y))
                self.steps += 1
                self.standing = self.steps
            else:
                if self.standing + 1 >= 30:
                    self.standing = 0
                if self.side < 0:
                    player = pl_standing_left[self.standing // 3]
                    player.set_colorkey((255, 255, 255))
                    window.blit(player, (self.x, self.y))
                elif self.side > 0:
                    player = pl_standing_right[self.standing // 3]
                    player.set_colorkey((255, 255, 255))
                    window.blit(player, (self.x, self.y))
                self.standing += 1
        else:
            self.hitbox = (0, 0, 0, 0)
            if self.death + 1 < 26:
                player = pl_death[self.death]
                player.set_colorkey((255, 255, 255))
                window.blit(player, (self.x, self.y))
                if self.death_loop > 0:
                    self.death_loop += 1
                if self.death_loop > 3:
                    self.death_loop = 0
                if self.death_loop == 0:
                    self.death += 1
            if self.death + 1 == 26:
                start_game = False
                restart_game()

        self.hitbox = (self.x + 105, self.y + 75, 40, 105)
        #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
        health_bar = health_bars[self.life]
        health_bar.set_colorkey((255, 255, 255))
        avatar.set_colorkey((255, 255, 255))
        window.blit(avatar, (10, 10))
        window.blit(health_bar, (60, 10))

    def hit(self):
        if self.life < 5:
            self.life += 1


class Bullet(object):
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.rad = 4
        self. color = ((226, 223, 223))
        self.velocity = 15 * side
        self.side = side

    def draw(self, window, color):
        pygame.draw.circle(window, color, (self.x, self.y), self.rad)

class Enemy(object):
    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.width = 128
        self.hight = 128
        self.end = end
        self.path = [self.x, self.end]
        self.steps = 0
        self.velocity = 2
        self.side = 1
        self.walk_right = list(map(lambda i: pygame.image.load(path.join(enemy_walk_sprites_dir, f'r{i}.png')), range(1,9)))
        self.walk_left = list(map(lambda i: pygame.image.load(path.join(enemy_walk_sprites_dir, f'l{i}.png')), range(1, 9)))
        self.hitbox = (self.x + 50, self.y + 40, 30, 60)
        self.vision = (self.x + 50, self.y + 40, 200, 30)
        self.life = 0
        self.death = 0
        self.bullets = list()
        self.particles = list()
        self.shoot_loop = 0

    def draw(self, window):
        if self.life < 5:
            self.move()
            if self.steps + 1 >= 24:
                self.steps = 0

            if self.velocity > 0:
                enemy = self.walk_right[self.steps // 3]
                self.steps += 1
            else :
                enemy = self.walk_left[self.steps // 3]
                self.steps += 1
            self.hitbox = (self.x + 50, self.y + 40, 30, 60)
            self.vision = (self.x + 50, self.y + 40, 300 * self.side, 30)
            #pygame.draw.rect(window, (255, 0, 0), self.hitbox, 2)
            #pygame.draw.rect(window, (255, 0, 0), self.vision)
            enemy.set_colorkey((255, 255, 255))
            health_bar = health_bars[self.life]
            health_bar = pygame.transform.scale(health_bar, (128, 128))
            health_bar.set_colorkey((255, 255, 255))
            window.blit(health_bar, (self.hitbox[0] - 5, self.hitbox[1] - 20))
            window.blit(enemy, (self.x, self.y))

            self.hitbox = (self.x + 50, self.y + 40, 30, 60)
            if self.velocity > 0:
                self.vision = (self.x + 50, self.y + 40, 200, 30)
            elif self.velocity < 0:
                self.vision = (self.x - 150, self.y + 40, 200, 30)

            if self.shoot_loop > 0:
                self.shoot_loop += 1
            if self.shoot_loop > 7:
                self.shoot_loop = 0

            if self.vision[0] < player.hitbox[0] and player.hitbox[0] + player.hitbox[2] < self.vision[0] + self.vision[2] and\
                self.vision[1] > player.hitbox[1] and self.vision[1] + self.vision[3] < player.hitbox[1] + player.hitbox[3]:
                if len(self.bullets) < 10 and self.shoot_loop == 0 :
                    self.bullets.append(Bullet(self.x + self.width // 2 + 25 * self.side, self.y + self.hight // 2 + 14, self.side))
                    for i in range(random.randint(5, 13)):
                        self.particles.append(Particle(self.x + self.width // 2 + 25 * self.side, self.y + self.hight // 2 + 14, self.side))
                    self.shoot_loop = 1
        else:
            if self.death + 1 <= 19:
                print('death')
                enemy = enemy_death[self.death]
                enemy.set_colorkey((255, 255, 255))
                window.blit(enemy, (self.x, self.y))
                self.death += 1

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.steps = 0
                self.side *= -1
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.side *= -1
                self.steps = 0
    def hit(self):
        if self.life < 5:
            self.life += 1

class Particle(object):
    def __init__(self, x1, y1, side):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1
        self.y2 = y1
        self.color = ((226, 223, 223))
        self.rad = random.randrange(1,3)
        self.velocityX = random.randint(0,17)
        self.velocityY = random.randint(2,17)
        self.sideX = side
        self.sideY = random.choice([1,-1])
        self.life = random.randint(20, 30)
    def draw(self, window, color):
        pygame.draw.circle(window, color, (self.x2, self.y2), self.rad)

class Fuel(object):
    def __init__(self, img, x, y):
        self.x = x
        self.y = y
        self.img = img
    def draw(self, img, x, y):
        window.blit(img, (x, y))

def draw_bg():
    window.fill(((255, 255, 255)))
    width = 2300
    for x in range(3):
        window.blit(sky, (x * width - bg_scroll * 0.01, 0))
        window.blit(mountaines1, (x * width - bg_scroll * 0.5, 0))
        window.blit(mountaines2, (x * width - bg_scroll * 0.7, 0))
        window.blit(ground, (x * width - bg_scroll * 0.9, 0))

def reDraw():
    if start_game:
        world.draw()
        player.draw(window)
    for enemy in enemies:
        enemy.draw(window)
        for bullet in enemy.bullets:
            bullet.draw(window, ((87, 94, 91)))
        for particle in enemy.particles:
            particle.draw(window, ((87, 94, 91)))
    for bullet in bullets:
        bullet.draw(window, ((226, 223, 223)))
    for particle in particles:
        particle.draw(window, ((226, 223, 223)))
    for fuel in fuels:
        fuel.draw(fuel.img, fuel.x, fuel.y)
    pygame.display.update()

def restart_game():
    global bullets, particles, enemies, shoot_loop
    bullets = list()
    particles = list()
    shoot_loop = 0
bullets = list()
fuels = list()
particles = list()
enemies = list()
shoot_loop = 0
start_game = False
clock = pygame.time.Clock()

world_data = list()
for row in range(ROWS):
    r = [-1] * MAX_COLS
    world_data.append(r)

with open(f'level{level}_data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for x, row in enumerate(reader):
        for y, tile in enumerate(row):
            world_data[x][y] = int(tile)

world = World()
player = world.process_data(world_data)

while running:

    clock.tick(30)
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 384 < mouse[0] < 616 and 550 < mouse[1] < 626:
                start_game = True


    if not start_game:

        draw_bg()
        window.blit(btn, (384, 550))
        window.blit(logo, (213, 280))
        pygame.display.update()
        restart_game()

    else:

        for bullet in bullets:
            if bullet.x > 10:
                bullet.x += bullet.velocity
            else:
                bullets.pop(bullets.index(bullet))
            for enemy in enemies:
                if bullet.y - bullet.rad < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.rad > enemy.hitbox[1]:
                    if bullet.x + bullet.rad > enemy.hitbox[0] and bullet.x - bullet.rad < enemy.hitbox[0] + enemy.hitbox[2]:
                        enemy.hit()
                        bullets.pop(bullets.index(bullet))
        for particle in particles:
            if ((particle.x2 - particle.x1)**2 + (particle.y2 - particle.y1)**2)**0.5 > particle.life:
                particles.pop(particles.index(particle))
            else:
                particle.x2 += particle.velocityX * particle.sideX
                particle.y2 += particle.velocityY * particle.sideY

        for enemy in enemies:
            for particle in enemy.particles:
                if ((particle.x2 - particle.x1)**2 + (particle.y2 - particle.y1)**2)**0.5 > particle.life:
                    enemy.particles.pop(enemy.particles.index(particle))
                else:
                    particle.x2 += particle.velocityX * particle.sideX
                    particle.y2 += particle.velocityY * particle.sideY
            for bullet in enemy.bullets:
                if bullet.x < 1000 and bullet.x > 0:
                    bullet.x += bullet.velocity
                if bullet.y - bullet.rad < player.hitbox[1] + player.hitbox[3] and bullet.y + bullet.rad > player.hitbox[1]:
                    if bullet.x + bullet.rad > player.hitbox[0] and bullet.x - bullet.rad < player.hitbox[0] + player.hitbox[2]:
                        player.hit()
                        enemy.bullets.pop(enemy.bullets.index(bullet))
                else:
                    enemy.bullets.pop(enemy.bullets.index(bullet))

        keys = pygame.key.get_pressed()

        if shoot_loop > 0:
            shoot_loop += 1
        if shoot_loop > 3:
            shoot_loop = 0

        if keys[pygame.K_f] and shoot_loop == 0:
            if len(bullets) < 10:
                bullets.append(Bullet(player.x + player.width//2 + 45*player.side, player.y + 126, player.side))
                for i in range(random.randint(5,13)):
                    particles.append(Particle(player.x + player.width//2 + 45*player.side, player.y + 126, player.side))
            shoot_loop = 1

        if keys[pygame.K_d]:
            player.x += player.velocity
            player.right = True
            player.left = False
            player.side = 1
        elif keys[pygame.K_a]:
            player.left = True
            player.right = False
            player.side = -1
            player.x -= player.velocity
        else:
            player.right = False
            player.left = False
            player.steps = 0
            scroll = 0
        if keys[pygame.K_SPACE]:
            player.is_jump = True
            player.right = False
            player.left = False
            player.steps = 0
        if player.is_jump:
            if player.jump_count >= -10:
                num = 1
                if player.jump_count < 0:
                    num = -1
                player.y -= (player.jump_count ** 2) * 0.5 * num
                player.jump_count -= 1
            else:
                player.is_jump = False
                player.jump_count = 10
        # if player.x > 1000 - SCROLL_FRAME or player.x < 100:
        #     scroll = player.velocity * player.side * -1
        #     bg_scroll -= scroll
        #     player.x -= player.velocity * player.side

        draw_bg()
        reDraw()
pygame.quit()
