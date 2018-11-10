import sys, pygame

pygame.init()

columns, rows = 6, 6
size = width, height = 800, 800
black = 0, 0, 0

screen = pygame.display.set_mode(size)

# ball = pygame.image.load("graphics\\floor_tile.png")
img = pygame.image.load("graphics\\floor_tile.png")
screen.fill(black)
for x in range(columns):
    for y in range(rows):
        xi, yi = x - y, (x + y) / 2
        tile = img.get_rect(center=(xi * 50 + 400, yi * 50 + 200))
        screen.blit(img, tile)

pygame.display.flip()
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
