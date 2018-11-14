import sys
import pygame

pygame.init()

size = width, height = 800, 800

screen = pygame.display.set_mode(size)
pygame.display.set_caption('BlockJoin')


def main():
    columns, rows = 6, 6
    img1 = pygame.image.load("graphics\\floor_tile1.png").convert()
    img1.set_colorkey((0, 0, 0))

    pill_s = pygame.image.load("graphics\\pillSp.png").convert()
    pill_s.set_colorkey((0, 0, 0))
    pill_w = pygame.image.load("graphics\\pillWp.png").convert()
    pill_w.set_colorkey((0, 0, 0))
    pill_n = pygame.image.load("graphics\\pillNp.png").convert()
    pill_n.set_colorkey((0, 0, 0))
    pill_e = pygame.image.load("graphics\\pillEp.png").convert()
    pill_e.set_colorkey((0, 0, 0))

    frog_e = pygame.image.load("graphics\\frogE.png").convert()
    frog_e.set_colorkey((0, 0, 0))
    frog_s = pygame.image.load("graphics\\frogS.png").convert()
    frog_s.set_colorkey((0, 0, 0))
    frog_w = pygame.image.load("graphics\\frogW.png").convert()
    frog_w.set_colorkey((0, 0, 0))
    frog_n = pygame.image.load("graphics\\frogN.png").convert()
    frog_n.set_colorkey((0, 0, 0))
    print('rap')

    xpos, ypos = 387, 222
    frog_img = frog_e
    frog = frog_img.get_rect(center=(xpos, ypos))
    while 1:
        draw_board(columns, rows, img1)
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_a]:
            xpos -= 50
            img2 = frog_w
        elif key[pygame.K_s]:
            ypos += 50
            img2 = frog_s
        elif key[pygame.K_d]:
            xpos += 50
            img2 = frog_e
        elif key[pygame.K_w]:
            ypos -= 50
            img2 = frog_n
        elif key[pygame.K_q]:
            sys.exit()
        xpos1, ypos1 = xpos - ypos, (xpos + ypos) / 2  # Transformation cartesian --> isometric
        frog.left, frog.top = xpos1, ypos1
        screen.blit(frog_img, frog)

        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(200)


def draw_board(columns, rows, img1):
    screen.fill((0, 0, 0))  # black
    for x in range(columns):
        for y in range(rows):
            xi, yi = x - y, (x + y) / 2  # Transformation cartesian --> isometric
            tile1 = img1.get_rect(center=(xi * 50 + 400, yi * 50 + 200))
            screen.blit(img1, tile1)


if __name__ == '__main__':
    main()
