import pygame
from os import path

pygame.init()
window = pygame.display.set_mode((1000, 1000))
img_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'walkSprites')
bg_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), 'bg')
running = True

walk_right = [pygame.image.load(path.join(img_dir, 'r1.png')), pygame.image.load(path.join(img_dir, 'r2.png')), pygame.image.load(path.join(img_dir, 'r3.png')),
              pygame.image.load(path.join(img_dir, 'r4.png')), pygame.image.load(path.join(img_dir, 'r5.png')), pygame.image.load(path.join(img_dir, 'r6.png')),
              pygame.image.load(path.join(img_dir, 'r7.png')), pygame.image.load(path.join(img_dir, 'r8.png')), pygame.image.load(path.join(img_dir, 'r9.png')),
              pygame.image.load(path.join(img_dir, 'r10.png'))]
walk_left = [pygame.image.load(path.join(img_dir, 'l1.png')), pygame.image.load(path.join(img_dir, 'l2.png')), pygame.image.load(path.join(img_dir, 'l3.png')),
              pygame.image.load(path.join(img_dir, 'l4.png')), pygame.image.load(path.join(img_dir, 'l5.png')), pygame.image.load(path.join(img_dir, 'l6.png')),
              pygame.image.load(path.join(img_dir, 'l7.png')), pygame.image.load(path.join(img_dir, 'l8.png')), pygame.image.load(path.join(img_dir, 'l9.png')),
              pygame.image.load(path.join(img_dir, 'l10.png'))]


player_properties = {
    'velocity': 5,
    'x': 100,
    'y': 700,
    'is_jump': False,
    'jump_count': 10,
    'left': False,
    'right': False,
    'steps': 0,
    'side': ''
}

def reDraw():
    global player_properties
    bg = pygame.image.load(path.join(bg_dir, 'bg.png'))
    bg = pygame.transform.scale(bg, (1000, 1000))
    window.blit(bg, (0,0))

    if player_properties['steps'] >= 33:
        player_properties['steps'] = 0
    else:
        if player_properties['right']:
            window.blit(walk_right[player_properties['steps'] // 3 - 1], (player_properties['x'], player_properties['y']))
            player_properties['steps'] += 1
        elif player_properties['left'] :
            window.blit(walk_left[player_properties['steps'] // 3 - 1], (player_properties['x'], player_properties['y']))
            player_properties['steps'] += 1
        else:
            if player_properties['side'] == 'left':
                window.blit(walk_left[0], (player_properties['x'], player_properties['y']))
            elif player_properties['side'] == 'right':
                window.blit(walk_right[0], (player_properties['x'], player_properties['y']))


    pygame.display.update()

clock = pygame.time.Clock()
while running:
    clock.tick(33)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        player_properties['x'] += player_properties['velocity']
        player_properties['right'] = True
        player_properties['left'] = False
        player_properties['side'] = 'right'
    elif keys[pygame.K_a]:
        player_properties['x'] -= player_properties['velocity']
        player_properties['left'] = True
        player_properties['right'] = False
        player_properties['side'] = 'left'
    else:
        player_properties['right'] = False
        player_properties['left'] = False
        player_properties['steps'] = 0
    if keys[pygame.K_SPACE]:
        player_properties['is_jump'] = True
        player_properties['right'] = False
        player_properties['left'] = False
        player_properties['steps'] = 0
    if player_properties['is_jump']:
        if player_properties['jump_count'] >= -10:
            num = 1
            if player_properties['jump_count'] < 0:
                num = -1
            player_properties['y'] -= (player_properties['jump_count'] ** 2) * 0.5 * num
            player_properties['jump_count'] -= 1
        else:
            player_properties['is_jump'] = False
            player_properties['jump_count'] = 10

    reDraw()
pygame.quit()
