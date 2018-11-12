import sys
import pygame

pygame.init()

size = width, height = 800, 800

screen = pygame.display.set_mode(size)
screen.set_colorkey((0, 0, 0))
pygame.display.set_caption('BlockJoin')


def main():
    columns, rows = 6, 6
    img1 = pygame.image.load("graphics\\floor_tile1.png").convert()
    img1.set_colorkey((0, 0, 0))
    # img2 = pygame.image.load("graphics\\cube1.png").convert()
    # img2.set_colorkey((0, 0, 0))
    frog_e = pygame.image.load("graphics\\frogE.png").convert()
    frog_e.set_colorkey((0, 0, 0))
    frog_s = pygame.image.load("graphics\\frogS.png").convert()
    frog_s.set_colorkey((0, 0, 0))
    frog_w = pygame.image.load("graphics\\frogW.png").convert()
    frog_w.set_colorkey((0, 0, 0))
    frog_n = pygame.image.load("graphics\\frogN.png").convert()
    frog_n.set_colorkey((0, 0, 0))

    xpos, ypos = 420, 220
    img2 = frog_e
    tile2 = img2.get_rect(center=(xpos, ypos))
    while 1:
        draw_board(columns, rows, img1)
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_a]:
            xpos -= 50
            img2 = frog_w
        if key[pygame.K_s]:
            ypos += 50
            img2 = frog_s
        if key[pygame.K_d]:
            xpos += 50
            img2 = frog_e
        if key[pygame.K_w]:
            ypos -= 50
            img2 = frog_n
        if key[pygame.K_q]:
            sys.exit()
        xpos1, ypos1 = xpos - ypos, (xpos + ypos) / 2  # Transformation cartesian --> isometric
        tile2.left, tile2.top = xpos1, ypos1
        screen.blit(img2, tile2)

        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(100)


def draw_board(columns, rows, img1):
    screen.fill((0, 0, 0))  # black
    for x in range(columns):
        for y in range(rows):
            xi, yi = x - y, (x + y) / 2  # Transformation cartesian --> isometric
            tile1 = img1.get_rect(center=(xi * 50 + 400, yi * 50 + 200))
            screen.blit(img1, tile1)


if __name__ == '__main__':
    main()
