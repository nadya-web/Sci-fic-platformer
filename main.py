import pygame
from os import path


pygame.init()
window = pygame.display.set_mode((1000, 1000))
running = True

img_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'walkSprites')
bg_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'bg')

walk_right = list(map(lambda i: pygame.image.load(path.join(img_dir, f'r{i}.png')), range(1, 12)))
walk_left = list(map(lambda i: pygame.image.load(path.join(img_dir, f'l{i}.png')), range(1, 12)))

class player(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 5
        self.is_jump = False
        self.jump_count = 10
        self.left = False
        self.right = False
        self.steps = 0
        self.side = 'right'

    def draw(self, window):
        if self.steps + 1 >= 30:
            self.steps = 0
        if self.right :
            player = walk_right[self.steps // 3]
            player.set_colorkey((255, 255, 255))
            window.blit(player, (self.x, self.y))
            self.steps += 1
        elif self.left:
            player = walk_left[self.steps // 3]
            player.set_colorkey((255, 255, 255))
            window.blit(player, (self.x, self.y))
            self.steps += 1
        else:
            if self.side == 'left' :
                player = walk_left[0]
                player.set_colorkey((255, 255, 255))
                window.blit(player, (self.x, self.y))
            elif self.side == 'right' :
                player = walk_right[0]
                player.set_colorkey((255, 255, 255))
                window.blit(player, (self.x, self.y))

player = player(100, 700)

def reDraw():
    bg = pygame.image.load(path.join(bg_dir, 'bg.png'))
    bg = pygame.transform.scale(bg, (1000, 1000))
    window.blit(bg, (0, 0))
    player.draw(window)
    pygame.display.update()

clock = pygame.time.Clock()
while running:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player.x += player.velocity
        player.right = True
        player.left = False
        player.side = 'right'
    elif keys[pygame.K_a]:
        player.x -= player.velocity
        player.left = True
        player.right = False
        player.side = 'left'
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
