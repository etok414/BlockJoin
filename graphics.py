import sys
import pygame


def initialize():
    pygame.init()

    size = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BlockJoin')

    graphics_dict = dict()

    graphics_dict['tile'] = pygame.image.load("graphics\\tile.png").convert()
    graphics_dict['tile'].set_colorkey((0, 0, 0))
    graphics_dict['tile_shadow1'] = pygame.image.load("graphics\\tile_shadow1.png").convert()
    graphics_dict['tile_shadow1'].set_colorkey((0, 0, 0))
    graphics_dict['tile_shadow2'] = pygame.image.load("graphics\\tile_shadow2.png").convert()
    graphics_dict['tile_shadow2'].set_colorkey((0, 0, 0))
    graphics_dict['tile_shadow3'] = pygame.image.load("graphics\\tile_shadow3.png").convert()
    graphics_dict['tile_shadow3'].set_colorkey((0, 0, 0))
    graphics_dict['tile_shadow4'] = pygame.image.load("graphics\\tile_shadow4.png").convert()
    graphics_dict['tile_shadow4'].set_colorkey((0, 0, 0))
    graphics_dict['tile_shadow5'] = pygame.image.load("graphics\\tile_shadow5.png").convert()
    graphics_dict['tile_shadow5'].set_colorkey((0, 0, 0))

    graphics_dict['pill_s'] = pygame.image.load("graphics\\pillS.png").convert()
    graphics_dict['pill_s'].set_colorkey((0, 0, 0))
    graphics_dict['pill_w'] = pygame.image.load("graphics\\pillW.png").convert()
    graphics_dict['pill_w'].set_colorkey((0, 0, 0))
    graphics_dict['pill_n'] = pygame.image.load("graphics\\pillN.png").convert()
    graphics_dict['pill_n'].set_colorkey((0, 0, 0))
    graphics_dict['pill_e'] = pygame.image.load("graphics\\pillE.png").convert()
    graphics_dict['pill_e'].set_colorkey((0, 0, 0))

    graphics_dict['blob_e'] = pygame.image.load("graphics\\frogE.png").convert()
    graphics_dict['blob_e'].set_colorkey((0, 0, 0))
    graphics_dict['blob_s'] = pygame.image.load("graphics\\frogS.png").convert()
    graphics_dict['blob_s'].set_colorkey((0, 0, 0))
    graphics_dict['blob_w'] = pygame.image.load("graphics\\frogW.png").convert()
    graphics_dict['blob_w'].set_colorkey((0, 0, 0))
    graphics_dict['blob_n'] = pygame.image.load("graphics\\frogN.png").convert()
    graphics_dict['blob_n'].set_colorkey((0, 0, 0))

    return graphics_dict, screen


def draw_board(width, height, tile, screen):
    screen.fill((0, 0, 0))  # black
    for x in range(width):
        for y in range(height):
            xi, yi = x - y, (x + y) / 2  # Transformation cartesian --> isometric
            tile1 = tile.get_rect(center=(xi * 50 + 400, yi * 50 + 200))
            screen.blit(tile, tile1)


def move_sprite_to(x_c, y_c, sprite, sprite_img, screen):
    x_i, y_i = transform(x_c, y_c)
    sprite.left, sprite.top = x_i, y_i
    screen.blit(sprite_img, sprite)


def transform(x_c, y_c):
    """ Transforms cartesian coordinates to isometric coordinates """
    x_i, y_i = x_c - y_c, (x_c + y_c) / 2
    return x_i, y_i


def main():
    graphics_dict, screen = initialize()
    draw_board(6, 6, graphics_dict['tile'], screen)
    while True:
        pilln = graphics_dict['pill_n']
        pille = graphics_dict['pill_e']
        pillw = graphics_dict['pill_w']
        pills = graphics_dict['pill_s']
        pill_n = pilln.get_rect(center=(0 * 50 + 400, 3 * 50 + 200))
        pill_e = pille.get_rect(center=(2 * 50 + 400, 2 * 50 + 200))
        pill_w = pillw.get_rect(center=(3 * 49 + 400, 3 * 41 + 200))
        pill_s = pills.get_rect(center=(1 * 60 + 400, 2 * 55 + 200))
        screen.blit(pilln, pill_n)
        screen.blit(pille, pill_e)
        screen.blit(pillw, pill_w)
        screen.blit(pills, pill_s)
        for event in pygame.event.get():  # Close nicely and display changes
            if event.type == pygame.QUIT:
                sys.exit()
        pygame.display.flip()
        pygame.time.delay(150)


if __name__ == '__main__':
    main()
