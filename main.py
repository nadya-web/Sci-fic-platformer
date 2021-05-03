import pygame
from os import path
import random


pygame.init()
window = pygame.display.set_mode((1000, 1000))
running = True

pl_walk_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pl_walk_sprites')
enemy_walk_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'enemy_walk')
standing_sprites_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'pl_standing_sprites')
bg_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'bg')

pl_walk_right = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_walk_left = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'l{i}.png')), range(1, 12)))
pl_standing_right = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_standing_left = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'l{i}.png')), range(1, 12)))

class Player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 256
        self.hight = 256
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.steps = 0
        self.standing = 0
        self.side = 1

    def draw(self, window):
        if self.steps + 1 >= 30:
            self.steps = 0
        if self.right:
            player = pl_walk_right[self.steps // 3]
            self.steps += 1
            self.standing = self.steps
        elif self.left:
            player = pl_walk_left[self.steps // 3]
            self.steps += 1
            self.standing = self.steps
        else:
            if self.standing + 1 >= 30:
                self.standing = 0
            if self.side < 0:
                player = pl_standing_left[self.standing // 3]
            elif self.side > 0:
                player = pl_standing_right[self.standing // 3]
            self.standing += 1
        player.set_colorkey((255, 255, 255))
        window.blit(player, (self.x, self.y))

class Bullet(object):
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.rad = 4
        self. color = ((226, 223, 223))
        self.velocity = 10 * side
        self.side = side

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.rad)

class Enemy(object):
    def __init__(self, x, y, end):
        self.x = x
        self.y = y
        self.width = 256
        self.hight = 256
        self.end = end
        self.path = [self.x, self.end]
        self.steps = 0
        self.velocity = 2
        self.walk_right = list(map(lambda i: pygame.image.load(path.join(enemy_walk_sprites_dir, f'r{i}.png')), range(1,9)))
        self.walk_left = list(map(lambda i : pygame.image.load(path.join(enemy_walk_sprites_dir, f'l{i}.png')), range(1, 9)))

    def draw(self, window):

        self.move()
        if self.steps + 1 >= 24:
            self.steps = 0

        if self.velocity > 0:
            enemy = self.walk_right[self.steps // 3]
            self.steps += 1
        else:
            enemy = self.walk_left[self.steps // 3]
            self.steps += 1

        enemy.set_colorkey((255, 255, 255))
        window.blit(enemy, (self.x, self.y))

    def move(self):
        if self.velocity > 0:
            if self.x + self.velocity < self.path[1]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.steps = 0
        else:
            if self.x - self.velocity > self.path[0]:
                self.x += self.velocity
            else:
                self.velocity *= -1
                self.steps = 0

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
    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x2, self.y2), self.rad)

def reDraw():
    bg = pygame.image.load(path.join(bg_dir, 'bg.png'))
    bg = pygame.transform.scale(bg, (1000, 1000))
    window.blit(bg, (0, 0))
    enemy.draw(window)
    player.draw(window)
    for bullet in bullets:
        bullet.draw(window)
    for particle in particles:
        particle.draw(window)
    pygame.display.update()

clock = pygame.time.Clock()
bullets = list()
particles = list()
player = Player(100, 700)
enemy = Enemy(400, 750, 800)
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for bullet in bullets:
        if bullet.x < 1000 and bullet.x > 0:
            bullet.x += bullet.velocity
        else:
            bullets.pop(bullets.index(bullet))
    for particle in particles:
        if ((particle.x2 - particle.x1)**2 + (particle.y2 - particle.y1)**2)**0.5 > particle.life:
            particles.pop(particles.index(particle))
        else:
            particle.x2 += particle.velocityX * particle.sideX
            particle.y2 += particle.velocityY * particle.sideY


    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if len(bullets) < 10:
            bullets.append(Bullet(player.x + player.width//2 + 45*player.side, player.y + 126, player.side))
            for i in range(random.randint(5,13)):
                particles.append(Particle(player.x + player.width//2 + 45*player.side, player.y + 126, player.side))

    if keys[pygame.K_d]:
        player.x += player.velocity
        player.right = True
        player.left = False
        player.side = 1
    elif keys[pygame.K_a]:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.side = -1
    else:
        player.right = False
        player.left = False
        player.steps = 0
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

    reDraw()
pygame.quit()
