import pygame
from os import path
import random


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

pl_walk_right = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_walk_left = list(map(lambda i: pygame.image.load(path.join(pl_walk_sprites_dir, f'l{i}.png')), range(1, 12)))
pl_standing_right = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'r{i}.png')), range(1, 12)))
pl_standing_left = list(map(lambda i: pygame.image.load(path.join(standing_sprites_dir, f'l{i}.png')), range(1, 12)))
pl_death = list(map(lambda i: pygame.image.load(path.join(pl_death_dir, f'{i}.png')), range(1, 27)))
enemy_death = list(map(lambda i: pygame.image.load(path.join(enemy_death_dir, f'{i}.png')), range(2, 21)))
health_bars = list(map(lambda i: pygame.image.load(path.join(pics_dir, f'{i}.png')), range(1,7)))
avatar = pygame.image.load(path.join(pics_dir, 'avatar.png'))
btn = pygame.image.load(path.join(pics_dir, 'start_btn.png'))
logo = pygame.image.load(path.join(pics_dir, 'logo.png'))

btn = pygame.transform.scale(btn, (232, 96))
logo = pygame.transform.scale(logo, (595, 230))
btn.set_colorkey((255, 255, 255))
logo.set_colorkey((255, 255, 255))

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
        self.velocity = 10 * side
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
            if self.steps + 1 >= 24 :
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
            if self.death + 1 < 20:
                enemy = enemy_death[self.death]
                enemy.set_colorkey((255, 255, 255))
                window.blit(enemy, (self.x, self.y))

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

def reDraw():
    bg = pygame.image.load(path.join(bg_dir, 'bg.png'))
    bg = pygame.transform.scale(bg, (1000, 1000))
    window.blit(bg, (0, 0))
    if start_game:
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
    pygame.display.update()

def restart_game():
    global player, bullets, particles, enemies, shoot_loop
    player = Player(100, 700)
    bullets = list()
    particles = list()
    enemies = [Enemy(400, 750, 600)]
    shoot_loop = 0
player = Player(100, 700)
bullets = list()
particles = list()
enemies = [Enemy(400, 750, 600)]
shoot_loop = 0
start_game = False
clock = pygame.time.Clock()
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

        bg = pygame.image.load(path.join(bg_dir, 'bg.png'))
        bg = pygame.transform.scale(bg, (1000, 1000))
        window.blit(bg, (0, 0))
        window.blit(btn, (384, 550))
        window.blit(logo, (213, 280))
        pygame.display.update()
        restart_game()

    else:
        for bullet in bullets:
            if bullet.x < 1000 and bullet.x > 0:
                bullet.x += bullet.velocity
            if bullet.y - bullet.rad < enemies[0].hitbox[1] + enemies[0].hitbox[3] and bullet.y + bullet.rad > enemies[0].hitbox[1]:
                if bullet.x + bullet.rad > enemies[0].hitbox[0] and bullet.x - bullet.rad < enemies[0].hitbox[0] + enemies[0].hitbox[2]:
                    enemies[0].hit()
                    bullets.pop(bullets.index(bullet))
            else:
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
