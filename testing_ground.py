import sys
import pygame

pygame.init()

size = width, height = 800, 800

screen = pygame.display.set_mode(size)
pygame.display.set_caption('BlockJoin')


def initialize():
    graphics_dict = dict()
    graphics_dict['tile'] = pygame.image.load("graphics\\floor_tile1.png").convert()
    graphics_dict['tile'].set_colorkey((0, 0, 0))

    graphics_dict['pill_s'] = pygame.image.load("graphics\\pillSp.png").convert()
    graphics_dict['pill_s'].set_colorkey((0, 0, 0))
    graphics_dict['pill_w'] = pygame.image.load("graphics\\pillWp.png").convert()
    graphics_dict['pill_w'].set_colorkey((0, 0, 0))
    graphics_dict['pill_n'] = pygame.image.load("graphics\\pillNp.png").convert()
    graphics_dict['pill_n'].set_colorkey((0, 0, 0))
    graphics_dict['pill_e'] = pygame.image.load("graphics\\pillEp.png").convert()
    graphics_dict['pill_e'].set_colorkey((0, 0, 0))

    graphics_dict['blob_e'] = pygame.image.load("graphics\\frogE.png").convert()
    graphics_dict['blob_e'].set_colorkey((0, 0, 0))
    graphics_dict['blob_s'] = pygame.image.load("graphics\\frogS.png").convert()
    graphics_dict['blob_s'].set_colorkey((0, 0, 0))
    graphics_dict['blob_w'] = pygame.image.load("graphics\\frogW.png").convert()
    graphics_dict['blob_w'].set_colorkey((0, 0, 0))
    graphics_dict['blob_n'] = pygame.image.load("graphics\\frogN.png").convert()
    graphics_dict['blob_n'].set_colorkey((0, 0, 0))

    return graphics_dict


def draw_board(columns, rows, tile):
    screen.fill((0, 0, 0))  # black
    for x in range(columns):
        for y in range(rows):
            xi, yi = x - y, (x + y) / 2  # Transformation cartesian --> isometric
            tile1 = tile.get_rect(center=(xi * 50 + 400, yi * 50 + 200))
            screen.blit(tile, tile1)


def main():
    graphics_dict = initialize()
    columns, rows = 6, 6
    xpos, ypos = 387, 222
    blob_img = graphics_dict['blob_e']
    pill_img = graphics_dict['pill_e']
    blob = blob_img.get_rect(center=(xpos, ypos))
    pill = pill_img.get_rect(center=(400, 250))
    while 1:
        draw_board(columns, rows, graphics_dict['tile'])
        pygame.event.pump()
        key = pygame.key.get_pressed()  # checking pressed keys
        if key[pygame.K_a]:
            xpos -= 50
            blob_img = graphics_dict['blob_w']
        elif key[pygame.K_s]:
            ypos += 50
            blob_img = graphics_dict['blob_s']
        elif key[pygame.K_d]:
            xpos += 50
            blob_img = graphics_dict['blob_e']
        elif key[pygame.K_w]:
            ypos -= 50
            blob_img = graphics_dict['blob_n']
        elif key[pygame.K_q]:
            sys.exit()
        xpos1, ypos1 = xpos - ypos, (xpos + ypos) / 2  # Transformation cartesian --> isometric
        blob.left, blob.top = xpos1, ypos1
        screen.blit(blob_img, blob)
        screen.blit(pill_img, pill)

        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
