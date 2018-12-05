import os
import sys
import pygame


def initialize():
    pygame.init()

    size = 800, 800
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('BlockJoin')

    graphics_dict = dict()  # A dictionary for all images with their filename as keys

    base_folder = os.path.dirname(__file__)
    folder = 'graphics'  # All graphics for the game have to go into this folder as .png or .PNG
    _path = os.path.join(base_folder, folder)
    path = os.path.normpath(_path)

    file_list = os.listdir(path)  # All files in the graphics directory is read into a list...

    for file_name in file_list:  # ...and only the .png files are loaded and stored in a dict with filename as key
        if file_name[-4:].lower() == '.png':
            _full_path = os.path.join(base_folder, folder, file_name)
            full_path = os.path.normpath(_full_path)

            graphics_dict[file_name[:-4]] = pygame.image.load(full_path).convert()
            graphics_dict[file_name[:-4]].set_colorkey((0, 0, 0))  # All black (0,0,0) is ignored (Pseudo alpha channel)

    return graphics_dict, screen


def draw_board(tile, screen):
    screen.fill((0, 0, 0))  # Black
    for x_c in range(6):
        for y_c in range(6):
            # x_i, y_i = x_c - y_c, (x_c + y_c) / 2
            tile.x_pos, tile.y_pos = x_c, y_c
            update_thing_pos(tile, screen)
            # tile1 = tile.get_rect(center=(x_i * 50 + 400, y_i * 50 + 200))
            # screen.blit(tile, tile1)


def update_thing_pos(thing, screen):
    screen_pos = dict(zip(('x', 'y'), thing.calc_screen_pos()))
    move_sprite_to(screen_pos['x'], screen_pos['y'], thing.rect, thing.image, screen)


def move_sprite_to(x_i, y_i, sprite, sprite_img, screen):
    sprite.left, sprite.top = 115 + x_i, 280 + y_i
    screen.blit(sprite_img, sprite)
    pygame.display.flip()


def main():
    """ Just for testing purposes """
    graphics_dict, screen = initialize()
    draw_board(6, 6, graphics_dict['tile'], screen)
    while True:
        pilln = graphics_dict['pillN']
        pille = graphics_dict['pillE']
        pillw = graphics_dict['pillW']
        pills = graphics_dict['pillS']
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
