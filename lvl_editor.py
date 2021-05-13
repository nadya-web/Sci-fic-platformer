import pygame
from os import path

pygame.init()

pics_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), "pics")
bg_dir = path.join(path.dirname("N:\python\Sci-fic-game\main.py"), "bg")

blocks = list(map(lambda i: pygame.image.load(path.join(pics_dir, f'block{i}.png')), range(1, 9)))
ground = pygame.image.load(path.join(bg_dir, 'ground.png'))
ground = pygame.transform.scale(ground, (2300, 1000))
ground.set_colorkey((255, 255, 255))
sky = pygame.image.load(path.join(bg_dir, 'sky.png'))
sky = pygame.transform.scale(sky, (2300, 1000))
sky.set_colorkey((255, 255, 255))
mountaines1 = pygame.image.load(path.join(bg_dir, 'mountaines1.png'))
mountaines1 = pygame.transform.scale(mountaines1, (2300, 1000))
mountaines1.set_colorkey((255, 255, 255))
mountaines2 = pygame.image.load(path.join(bg_dir, 'mountaines2.png'))
mountaines2 = pygame.transform.scale(mountaines2, (2300, 1000))
mountaines2.set_colorkey((255, 255, 255))

window = pygame.display.set_mode((1000 + 300, 1000))
clock = pygame.time.Clock()
running = True

ROWS = 20
MAX_COLS = 150
TILE_SIZE = 1300 // ROWS

scroll_left = False
scroll_right = False
scroll_velocity = 1
scroll = 0

class Button(object):
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img

    def draw(self):
        window.blit(self.img, (self.x, self.y))

def draw_grid():
    global MAX_COLS, ROWS, TILE_SIZE
    for col in range(MAX_COLS + 1):
        pygame.draw.line(window, (255, 255, 255), (col * TILE_SIZE + scroll, 0), (col * TILE_SIZE + scroll, 1000))
    for row in range(ROWS + 1):
        pygame.draw.line(window, (255, 255, 255), (0, row * TILE_SIZE), (2300, row * TILE_SIZE))

def draw():
    clock.tick(30)
    window.fill(((255, 255, 255)))
    width = 2300
    for x in range(3):
        window.blit(sky, ((x * width) + scroll * 0.01, 0))
        window.blit(mountaines1, ((x * width) + scroll * 0.5, 0))
        window.blit(mountaines2, ((x * width) + scroll * 0.7, 0))
        window.blit(ground, ((x * width) + scroll * 0.9, 0))

def draw_btns():
    pygame.draw.rect(window, (255, 255, 255), (970, 0, 1300, 1000))
    for btn in buttons:
        btn.draw()

def draw_rect(x, y):
    pygame.draw.rect(window, (186, 74, 74), (x, y, 64, 64), 5)

buttons = list()
button_selected = [975, 260]

for block in blocks:
    row = len(buttons) % 3
    col = len(buttons) // 3
    block = pygame.transform.scale(block, (64, 64))
    block.set_colorkey((255, 255, 255))
    buttons.append(Button(975 + 128 * row, 260 + 128 * col, block))

while running:

    if scroll_left and scroll < 0:
        scroll += 15 * scroll_velocity
    if scroll_right:
        scroll -= 15 * scroll_velocity

    draw()
    draw_grid()
    draw_btns()
    draw_rect(button_selected[0], button_selected[1])

    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                scroll_right = True
            if event.key == pygame.K_a:
                scroll_left = True
            if event.key == pygame.K_LSHIFT:
                scroll_velocity = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d:
                scroll_right = False
            if event.key == pygame.K_a:
                scroll_left = False
            if event.key == pygame.K_LSHIFT:
                scroll_velocity = 1
        if event.type == pygame.MOUSEBUTTONDOWN:
            for btn in buttons:
                if btn.x < mouse[0] < btn.x + 64 and \
                    btn.y < mouse[1] < btn.y + 64:
                    button_selected[0] = btn.x
                    button_selected[1] = btn.y

    pygame.display.update()

pygame.quit()
